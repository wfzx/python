#conding:utf-8

import os
import sys

if len(sys.argv) < 4:
    print("请输入以下几个参数（顺序不可乱）: 环境,前端或后端,jenkins的项目名称,项目名称")
    sys.exit(1)
else:
    Env = sys.argv[1]
    FrontEndOrBackEnd = sys.argv[2]
    JenkinsWorkspaceName = sys.argv[3]
    ProjectName = sys.argv[4]
    if FrontEndOrBackEnd == "java":
        ExecReleaseProcessCmd = "python3 /data/release/release.py %s %s %s" % (JenkinsWorkspaceName,ProjectName,Env)
    else:
        ExecReleaseProcessCmd = "python3 /data/release/h5.py %s %s %s" % (JenkinsWorkspaceName,ProjectName,Env)