from django.db import models

class AddServerLog(models.Model):
    Project = models.CharField(max_length=32)
    Node = models.CharField(max_length=128)
    Port = models.CharField(max_length=6)
    MemSize = models.CharField(max_length=6)
    CheckOpsApi = models.CharField(max_length=128)
    ServerType = models.CharField(max_length=6)
    ReSet = models.CharField(max_length=4)
    CreateTime = models.CharField(max_length=20)
    Remarks = models.CharField(max_length=128, null=True)
    Belong = models.CharField(max_length=8,null=True)

    def __str__(self):
        return self.Project

class ModifyServerLog(models.Model):
    Project = models.CharField(max_length=32)
    Node = models.CharField(max_length=128, null=True)
    Port = models.CharField(max_length=6, null=True)
    MemSize = models.CharField(max_length=6, null=True)
    CheckOpsApi = models.CharField(max_length=128)
    ServerType = models.CharField(max_length=6)
    ReSet = models.CharField(max_length=4)
    ModifyTime = models.CharField(max_length=20)
    Remarks = models.CharField(max_length=128, null=True)
    ModifyUser = models.CharField(max_length=32)
    EnvPar = models.CharField(max_length=8, null=True)
    Belong = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.Project

class EnvInfo(models.Model):
    EnvPar = models.CharField(max_length=8, null=True)
    ServerUser = models.CharField(max_length=12)
    ServerPass = models.CharField(max_length=32)
    RepoAddress = models.CharField(max_length=64)
    RepoUser = models.CharField(max_length=64)
    RepoPass = models.CharField(max_length=64)
    JenkinsDir = models.CharField(max_length=128)
    RootDir = models.CharField(max_length=64)
    BackupDir = models.CharField(max_length=64)
    EurekaAddress = models.CharField(max_length=64)
    Hosts = models.TextField(max_length=1024)
    JavaStartPar = models.TextField(max_length=1024)
    SkywalkingAddress = models.TextField(max_length=1024)
    TenDir = models.CharField(max_length=64)
    ModifyTime = models.CharField(max_length=20, null=True)
    CreateTime = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.ServerUser

class ModifyEnvLog(models.Model):
    EnvPar = models.CharField(max_length=8, null=True)
    ServerUser = models.CharField(max_length=12)
    ServerPass = models.CharField(max_length=32)
    RepoAddress = models.CharField(max_length=64)
    RepoUser = models.CharField(max_length=64)
    RepoPass = models.CharField(max_length=64)
    JenkinsDir = models.CharField(max_length=128)
    RootDir = models.CharField(max_length=64)
    BackupDir = models.CharField(max_length=64)
    EurekaAddress = models.CharField(max_length=64)
    Hosts = models.TextField(max_length=1024)
    ModifyTime = models.CharField(max_length=20, null=True)
    Remarks = models.CharField(max_length=128, null=True)
    ModifyUser = models.CharField(max_length=32)

    def __str__(self):
        return self.ServerUser

class AddEnvLog(models.Model):
    EnvPar = models.CharField(max_length=8, null=True)
    ServerUser = models.CharField(max_length=12)
    ServerPass = models.CharField(max_length=32)
    RepoAddress = models.CharField(max_length=64)
    RepoUser = models.CharField(max_length=64)
    RepoPass = models.CharField(max_length=64)
    JenkinsDir = models.CharField(max_length=128)
    RootDir = models.CharField(max_length=64)
    BackupDir = models.CharField(max_length=64)
    EurekaAddress = models.CharField(max_length=64)
    Hosts = models.TextField(max_length=1024)
    CreateTime = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.ServerUser

class ProjectInfo(models.Model):
    Project = models.CharField(max_length=32)
    EnvPar = models.CharField(max_length=8, null=True)
    Node = models.CharField(max_length=128)
    Port = models.CharField(max_length=6)
    MemSize = models.CharField(max_length=6)
    CheckOpsApi = models.CharField(max_length=128, null=True)
    ServerType = models.CharField(max_length=6, null=True)
    ReSet = models.CharField(max_length=4, null=True)
    Del = models.CharField(max_length=2)
    TenProxy = models.CharField(max_length=2)
    ReTengine = models.CharField(max_length=2)
    AddSkywalking = models.CharField(max_length=2)
    ProjectStatus = models.CharField(max_length=1024,null=True)
    OldNodeRm = models.CharField(max_length=2,default=0)
    OldNode = models.CharField(max_length=128,null=True)
    OldPort = models.CharField(max_length=6,null=True)
    ModifyTime = models.CharField(max_length=20, null=True)
    CreateTime = models.CharField(max_length=20, null=True)
    ReleaseTime = models.CharField(max_length=20, null=True)
    CheckApiTime = models.CharField(max_length=20, null=True)
    Belong = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.Project

class EnvConnInfo(models.Model):
    EnvPar = models.CharField(max_length=8, null=True, default=0)
    KafkaInt = models.CharField(max_length=256, null=True, default=0)
    KafkaExt = models.CharField(max_length=256, null=True, default=0)
    HbaseInt = models.CharField(max_length=256, null=True, default=0)
    HbaseExt = models.CharField(max_length=256, null=True, default=0)
    HbaseUser = models.CharField(max_length=32, null=True, default=0)
    HbasePass = models.CharField(max_length=128, null=True, default=0)
    MysqlInt = models.CharField(max_length=256, null=True, default=0)
    MysqlExt = models.CharField(max_length=256, null=True, default=0)
    MysqlUser = models.CharField(max_length=32, null=True, default=0)
    MysqlPass = models.CharField(max_length=128, null=True, default=0)
    RedisInt = models.CharField(max_length=256, null=True, default=0)
    RedisExt = models.CharField(max_length=256, null=True, default=0)
    RedisPass = models.CharField(max_length=128, null=True, default=0)
    CreateTime = models.CharField(max_length=20, null=True, default=0)
    ModifyTime = models.CharField(max_length=20)

    def __str__(self):
        return self.EnvPar

class AddEnvConnLog(models.Model):
    EnvPar = models.CharField(max_length=8, null=True)
    KafkaInt = models.CharField(max_length=256, null=True, default=0)
    KafkaExt = models.CharField(max_length=256, null=True, default=0)
    HbaseInt = models.CharField(max_length=256, null=True, default=0)
    HbaseExt = models.CharField(max_length=256, null=True, default=0)
    HbaseUser = models.CharField(max_length=32, null=True, default=0)
    HbasePass = models.CharField(max_length=128, null=True, default=0)
    MysqlInt = models.CharField(max_length=256, null=True, default=0)
    MysqlExt = models.CharField(max_length=256, null=True, default=0)
    MysqlUser = models.CharField(max_length=32, null=True, default=0)
    MysqlPass = models.CharField(max_length=128, null=True, default=0)
    RedisInt = models.CharField(max_length=256, null=True, default=0)
    RedisExt = models.CharField(max_length=256, null=True, default=0)
    RedisPass = models.CharField(max_length=128, null=True, default=0)
    CreateTime = models.CharField(max_length=20, null=True, default=0)
    ModifyTime = models.CharField(max_length=20)

    def __str__(self):
        return self.EnvPar

class ModifyEnvConnLog(models.Model):
    EnvPar = models.CharField(max_length=8, null=True, default=0)
    KafkaInt = models.CharField(max_length=256, null=True, default=0)
    KafkaExt = models.CharField(max_length=256, null=True, default=0)
    HbaseInt = models.CharField(max_length=256, null=True, default=0)
    HbaseExt = models.CharField(max_length=256, null=True, default=0)
    HbaseUser = models.CharField(max_length=32, null=True, default=0)
    HbasePass = models.CharField(max_length=128, null=True, default=0)
    MysqlInt = models.CharField(max_length=256, null=True, default=0)
    MysqlExt = models.CharField(max_length=256, null=True, default=0)
    MysqlUser = models.CharField(max_length=32, null=True, default=0)
    MysqlPass = models.CharField(max_length=128, null=True, default=0)
    RedisInt = models.CharField(max_length=256, null=True, default=0)
    RedisExt = models.CharField(max_length=256, null=True, default=0)
    RedisPass = models.CharField(max_length=128, null=True, default=0)
    ModifyTime = models.CharField(max_length=20)
    ModifyUser = models.CharField(max_length=32)

    def __str__(self):
        return self.EnvPar

class CronExecReco(models.Model):
    ExecTime = models.CharField(max_length=64)
    Who = models.CharField(max_length=32)

    def __str__(self):
        return self.ExecTime