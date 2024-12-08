from celery import group
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse
from .dependencies import get_async_session

from service import universities
from celery_tasks.tasks import get_all_universities_task, get_university_task
from config.celery_utils import get_task_info
from schemas.schemas import Country, CountryResponse
from models.universities import Country as CountryModel
from service.producer import send_task_to_queue

router = APIRouter(
    prefix="/universities",
    tags=["University"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def get_universities(country: Country) -> dict:
    """
    Return the List of universities for the countries for e.g ["turkey","india","australia"] provided
    in input in a sync way
    """
    data: dict = {}
    for cnt in country.countries:
        data.update(universities.get_all_universities_for_country(cnt))
    return data


@router.post("/async")
async def get_universities_async(country: Country):
    """
    Return the List of universities for the countries for e.g ["turkey","india","australia"] provided
    in input in a async way. It just returns the task id, which can later be used to get the result.
    """
    task = get_all_universities_task.apply_async(args=[country.countries])
    return JSONResponse({"task_id": task.id})


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)


@router.post("/parallel")
async def get_universities_parallel(country: Country) -> dict:
    """
    Return the List of universities for the countries for e.g ["turkey","india","australia"] provided
    in input in a sync way. This will use Celery to perform the subtasks in a parallel manner
    """

    data: dict = {}
    tasks = []
    for cnt in country.countries:
        tasks.append(get_university_task.s(cnt))
    # create a group with all the tasks
    job = group(tasks)
    result = job.apply_async()
    ret_values = result.get(disable_sync_subtasks=False)
    for result in ret_values:
        data.update(result)
    return data


@router.post("/fetch-data/{country}")
async def fetch_data(country: str):
    try:
        await send_task_to_queue(country)
        return JSONResponse(
            {"message": f"Task for {country} has been sent to the queue"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@router.get("/countries/{country_id}", response_model=CountryResponse)
async def get_country(
    country_id: int, session: AsyncSession = Depends(get_async_session)
):
    print("---- session -----", type(session))
    # Query the database for the country
    query = select(CountryModel).where(CountryModel.id == country_id)
    result = await session.execute(query)
    country = result.scalars().first()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Include related universities if needed
    return CountryResponse(
        id=country.id,
        name=country.name,
        alpha_two_code=country.alpha_two_code,
        universities=[uni.name for uni in country.universities],
    )
