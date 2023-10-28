from rest_framework.response import Response

class Responses(object):
    def __init__(self,status_code,data=None,message=None,headers=None) -> None:
        # super().__init__(status_code,data,headers)
        self.status_code=status_code
        self.data=data
        self.message=message

    def success_message(self):
        return Response(
            data={
                "message":"success",
                'data':self.data,
                "status":"success"
            },
            status=self.status_code
        )
        
 

    def error_message(self):
        raise 