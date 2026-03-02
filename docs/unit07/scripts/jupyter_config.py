c = get_config()
c.IPKernelApp.pylab = "inline"  # if you want plotting support always
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_origin = "*"
c.ServerApp.allow_remote_access = True
