from pydantic import BaseModel


class AllProduct(BaseModel):
    name :str
    description : str
    price : float
    stock_quantity : int