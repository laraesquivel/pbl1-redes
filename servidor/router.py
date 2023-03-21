class Router:
    routes = {}

    @classmethod
    def route(cls,path):
        def decoretor(fn):
            cls.routes[path] = fn
            return fn
        return decoretor
    
    @classmethod
    def dispath(cls,path):
        view = cls.routes.get(path)
        if view:
            return view()
        return None