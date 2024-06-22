from werkzeug.wrappers import Request, Response, ResponseStream


class Middleware:
    def __init__(self, app):
        self.app = app
        self.username = "rrtraders"
        self.password = "pass123"
        
    def __call__(self, environ, start_response):
        try: 
            request = Request(environ)
            username = request.authorization['username']
            password = request.authorization['password']
            if username == self.username and password == self.password:
                environ['user'] = {
                    'name': 'rrtraders'
                }
                return self.app(environ, start_response)
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)
        except Exception as e:
            res = Response(u'Authorization required', mimetype='text/plain', status=500)
            return res(environ, start_response)            
        