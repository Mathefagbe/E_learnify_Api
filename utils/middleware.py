from typing import Any


class TestMiddleWare(object):
    def __init__(self,get_response) -> None:
        self.get_response=get_response
     

    def __call__(self,request) -> Any:
        response=self.get_response(request)
        return response
    
    def process_view(self,request,view_func,view_args,view_kwrags):
        pass
