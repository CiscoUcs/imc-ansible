# This file needs to be copied to ansible module_utils
try:
    import imcsdk
    HAS_IMCSDK = True
except:
    HAS_IMCSDK = False


class ImcConnection():

    @staticmethod
    def is_login_param(param):
        return param in ["ip", "username", "password",
                         "port", "secure", "proxy", "server"]

    def __init__(self, module):
        if HAS_IMCSDK is False:
            results = {}
            results["msg"] = "imcsdk is not installed"
            module.fail_json(**results)
        self.module = module
        self.handle = None

    def login(self):
        ansible = self.module.params
        server = ansible.get('server')
        if server:
            return server

        from imcsdk.imchandle import ImcHandle
        results = {}
        try:
            server = ImcHandle(ip=ansible["ip"],
                               username=ansible["username"],
                               password=ansible["password"],
                               port=ansible["port"],
                               secure=ansible["secure"],
                               proxy=ansible["proxy"])
            server.login()
        except Exception as e:
            results["msg"] = str(e)
            self.module.fail_json(**results)
        self.handle = server
        return server

    def logout(self):
        server = self.module.params.get('server')
        if server:
            # we used a pre-existing handle from a task.
            # do not logout
            return False

        if self.handle:
            self.handle.logout()
            return True
        return False
