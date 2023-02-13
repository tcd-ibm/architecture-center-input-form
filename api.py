'''API v1 for the database'''
from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse
from cache import AsyncTTL

import aiosqlite
import ast

router = APIRouter()


def tryEval(val):
    try:
        return ast.literal_eval(val)
    except ValueError:
        return val


@AsyncTTL(time_to_live=60, maxsize=64)
async def fetch_all(table: str, params: dict = None):
    global db
    where = '' if not params else ' WHERE ' + ' AND '.join(
        [f'{key} = {tryEval(value)}' for key, value in params.items()])
    async with db.execute(f'SELECT * FROM {table}' + where) as cursor:
        values = await cursor.fetchall()
        results = [
            dict(line) for line in [
                zip([column[0] for column in cursor.description], row)
                for row in values
            ]
        ]
        return results


async def post_all(table: str, data: dict = None):
    if not dict:
        return

    for key, value in data.items():
        if isinstance(value, str):
            data[key] = tryEval(value)

    global db
    columns = ','.join(data.keys())
    values = ','.join(data.values())
    try:
        async with db.execute(
                f'INSERT INTO {table} ({columns}) VALUES ({values})'):
            await db.commit()
    except Exception as e:
        print(e)


@router.on_event("startup")
async def startup():
    global db
    db = await aiosqlite.connect("database/database.db")
    assert isinstance(db, aiosqlite.Connection)


@router.on_event("shutdown")
async def shutdown():
    await db.close()


@router.post("/announcements", response_class=UJSONResponse)
async def create_announcement(request: Request):
    await post_all("AnnouncementList", request.query_params._dict)
    return UJSONResponse(content={"status": "success"})


@router.get("/announcements", response_class=UJSONResponse)
async def fetch_announcement(request: Request):
    r = await fetch_all("AnnouncementList", request.query_params._dict)
    return UJSONResponse(content=r)


@router.post("/detail", response_class=UJSONResponse)
async def create_detail(request: Request):
    data = request.query_params._dict
    await post_all("DetailLink", data)
    return UJSONResponse(content={"status": "success"})


@router.get("/detail/{ppid}", response_class=UJSONResponse)
async def fetch_detail(request: Request, ppid: int = 0):
    data = request.query_params._dict
    if ppid:
        data.update({"ppid": ppid})
    r = await fetch_all("DetailLink", data)
    return UJSONResponse(content=r)


@router.post("/pa", response_class=UJSONResponse)
async def create_pa(request: Request):
    await post_all("PAList", request.query_params._dict)
    return UJSONResponse(content={"status": "success"})


@router.get("/pa/{ppid}", response_class=UJSONResponse)
async def fetch_pa(request: Request, ppid: int = 0):
    data = request.query_params._dict
    if ppid:
        data.update({"ppid": ppid})
    r = await fetch_all("PAList", data)
    return UJSONResponse(content=r)


@router.post("/product", response_class=UJSONResponse)
async def create_product(request: Request):
    await post_all("ProductList", request.query_params._dict)
    return UJSONResponse(content={"status": "success"})


@router.get("/product", response_class=UJSONResponse)
async def fetch_product(request: Request):
    r = await fetch_all("ProductList", request.query_params._dict)
    return UJSONResponse(content=r)


@router.post("/solution", response_class=UJSONResponse)
async def create_solution(request: Request):
    data = request.query_params._dict
    await post_all("SolutionList", data)
    return UJSONResponse(content={"status": "success"})


@router.get("/solution", response_class=UJSONResponse)
async def fetch_solution(request: Request):
    r = await fetch_all("SolutionList", request.query_params._dict)
    return UJSONResponse(content=r)


@router.post("/type", response_class=UJSONResponse)
async def create_type(request: Request):
    await post_all("TypeList", request.query_params._dict)
    return UJSONResponse(content={"status": "success"})


@router.get("/type", response_class=UJSONResponse)
async def fetch_type(request: Request):
    r = await fetch_all("TypeList", request.query_params._dict)
    return UJSONResponse(content=r)


@router.post("/vertical", response_class=UJSONResponse)
async def create_vertical(request: Request):
    await post_all("VerticalList", request.query_params._dict)
    return UJSONResponse(content={"status": "success"})


@router.get("/vertical", response_class=UJSONResponse)
async def fetch_vertical(request: Request):
    r = await fetch_all("VerticalList", request.query_params._dict)
    return UJSONResponse(content=r)


'''
async def search(request: Request, table: str = None, mode: str = None):
    if not table:
        return UJSONResponse(content={"status": "error"})

    r = await fetch_all(table)
    params = request.query_params._dict
    if not params:
        return UJSONResponse(content=r)

    results = []
    try:
        for i in r:
            valid = True
            for k in params.keys():
                if tryEval(i[k]) != tryEval(params[k]):
                    valid = False
                    break
            if valid:
                results.routerend(i)
                if mode == "first":
                    break
    except KeyError as e:
        return UJSONResponse(content={"KeyError": str(e)})

    return UJSONResponse(content=results)
'''
