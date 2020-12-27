[![pipeline status](https://gitlab.com/tnt_boom/python-ci-gitlab/badges/master/pipeline.svg)](https://gitlab.com/tnt_boom/python-ci-gitlab/commits/master) 
[![coverage report](https://gitlab.com/tnt_boom/python-ci-gitlab/badges/master/coverage.svg)](https://gitlab.com/tnt_boom/python-ci-gitlab/commits/master)

# Before everything
- CD (Continuous Delivery): **注意** 因為這個 projets 在 gitlab 並沒有和任何系統串接, 所以沒有做到 CD, 請注意
- 能否支援 Spark: 目前暫時僅支援 Spark local mode @@
    - 測試使用的 docker image 的 spark 安裝目錄: `/opt/spark/latest`
    - pyspark 路徑: `/opt/spark/latest/bin/` 中可以看到 pyspark
     
## Docker image package info
- OpenJDK 8
- Python 2 and Python 3
- spark-2.4.3-hadoop-2.7
- CentOS 7.6

# python-ci-gitlab
- Sample codes for gitlab CI

# Folder structure

```
 .coveragerc: 在 pytest --cov=cathay/ tests 想要跳過不測試的檔案
 .gitlab-ci.yml: gitlab CI 的設定檔案, 詳見下文
 pytest.ini: 執行 pytest 時的參數
 requirements: 列出執行前要裝的所有 python packages, pytest/pytest-cov/pytest-xdist/pytest-bdd 是執行測試時會用的
 cathay: 分析或是應用程式放置的地方
   `- __init__.py
   `- sample
         `- __init__.py
         `- core.py: main class that processes Customer
         `- customer.py: this includes Customer class
 docs: documentation
 tests: all test codes. I use pytest here.
    `- README.md: description about this folder
    `- __init__.py
    `- conftest.py: 如果測試期間會共用的設定可以放在這個檔案
    `- test_core.py: 測試程式範例, 在這邊會驗證 core.py 的各個 function (deposit/withdraw/add_interest)
 gitlab-ci.yml_example: 
    `- python2: 如果您程式屬於 Python 2, 請用這個目錄下面的 .gitlab-ci.yml
         `-.gitlab-ci.yml.private: 如果專案權限是 private 或是 internal, 會使用這個檔案
         `- .gitlab-ci.yml.public: 如果專案權限是 public, 會使用這個檔案
    `- python3: 如果您程式屬於 Python 3, 請用這個目錄下面的 .gitlab-ci.yml
         `-.gitlab-ci.yml.private: 如果專案權限是 private 或是 internal, 會使用這個檔案
         `- .gitlab-ci.yml.public: 如果專案權限是 public, 會使用這個檔案
```


# 怎樣設定 gitlab CI
## 前言
- 第一步: 思考專案權限, 設定專案權限, 放置 .gitlab-ci.yml 到對應檔案路徑, 請參考 `思考 gitlab project permission` , 如果是 public, 請看 `如果專案是 public 的話` , 如果專案是 private 或是 internal, 請看 `如果專案是 internal 或是 private`
- 第二步: 請看 `Runner 設定` 
- 第三步: 請看 `code coverage`
- 第四步: 請查看 `執行測試並查看 code coverage`
- 第五步: 請查看 `如果想要看到 gitlab badge`
- 第六步: 如果需要確認 source codes 有沒有安全的問題, 請參考 `Security Scan`
- 第七步: 如果寫的是module, 需要上傳到 Nexus, 就請參考 `Module 上傳到 Nexus`

## 思考 gitlab project permission
- 如果有資安疑慮, 應該在 gitlab 上使用 internal/private project permission
- 如果沒有資安疑慮, gitlab project 設定上面就可以使用 public 權限, .gitlab-ci.yml 的 image 這個項目也可以直接指定像是 `image: python3.7` 的 docker image
- 以上兩種的設定區別有
    - gitlab 專案設定
    - 所使用的 .gitlab-ci.yml

## 如果專案是 public 的話
### 確認 gitlab 專案設定
- 編輯 gitlab 網頁畫面: `Settings` -> `General` -> `Visibility, project features, permissions` 請確認為 `Public` 如果不是, 請改成 `Public`

### .gitlab-ci.yml
- 請把 gitlab-ci.yml_example/.gitlab-ci.yml.public 放到專案最上層, 假設您的專案目錄是現在這個工作目錄 (./), 那麼請執行下面指令

```

$ cp gitlab-ci.yml_example/pythonX/.gitlab-ci.yml.public ./.gitlab-ci.yml  
#  pythonX: 如果開發時是 Python 2, 這邊即為 python2, 若用 Python 3 開發, 這邊就是 python3

```
## 如果專案是 internal 或是 private
### 確認 gitlab 專案設定
- 編輯 gitlab 網頁畫面: `Settings` -> `General` -> `Visibility, project features, permissions` 請確認為 `Internal` 或是 `Private` (請依照需求選擇是 internal 還是 private)
- **使用我們自己包的 docker image** 如果您要用的 docker image 是放在 private docker registry, 請在 gitlab 網頁上面, 左邊 `Settings` -> `CI/CD` 看右邊 Variables 定
義
    - input variable key 請寫 `DOCKER_AUTH_CONFIG`
    - input variable value 請寫 (沒錯, 就是這麼複雜)
```
{
        "auths": {
                "https://index.docker.io/v1/": {
                        "auth": "dG50Ym9vbTpjYXRoYXlnb2dvZ28="
                }
        },
        "HttpHeaders": {
                "User-Agent": "Docker-Client/18.06.1-ce (linux)"
        }
}
```

### .gitlab-ci.yml
- 請把 gitlab-ci.yml_example/.gitlab-ci.yml.internal 放到專案最上層, 假設您的專案目錄是現在這個工作目錄 (./), 那麼請執行下面指令

```
$ cp gitlab-ci.yml_example/pythonX/.gitlab-ci.yml.private ./.gitlab-ci.yml  
#  pythonX: 如果開發時是 Python 2, 這邊即為 python2, 若用 Python 3 開發, 這邊就是 python3
```

## Runner 設定
- 目前已經有一個用 k8s 裝的 gitlab runner 放在 AWS EC2 上面, 如果要用這個 gitlab runner, 在 project 的設定很簡單, 只要在gitlab 專案中 Settings -> CI/CD -> 右邊視窗中的 `Runners` 中的 `Shared Runners` 要選擇 `Disable shared Runners` 就可以
- 
### 備註: Shared Runner 
- gitlab 免費版本在每一個 group 中所有 private project 一個月能夠使用 shared runner 2000 分鐘的 CI 時間, 超過就要付錢
- 我們之前使用 Shared runner, 使用方式很間單, 只要將加上 `.gitlab-ci.yml` 和 project 設定一下就完成了, 剩下就是要小心全部 private project 所執行的 CI 時間不要一個月跑超過 2000 分鐘就好


## code coverage
- 打開 `.gitlab-ci.yml` 只要看到 `pytest --cov=cathay/ tests` 就會跑出 code coverage, 就完成設定
- 在 gitlab 網頁上面, 左邊 `Settings` -> `CI/CD` ,  右邊 `General pipelines` 中有一個 `Test coverage parsing` 請填上 `^TOTAL\s+\d+\s+\d+\s+(\d+\%)$` (其實下方案例有)
- 就可以按下 `Save changes`

## 執行測試並查看 code coverage
- 將程式碼放到 gitlab 後, 可以透過左邊的 `CI/CD` -> `Jobs` 看到每一個 job 執行狀況, 如果沒有設定錯誤, 應該會看到 `Coverage` 是有數字的

## 如果想要看到 gitlab badge
- 範例: [![pipeline status](https://gitlab.com/tnt_boom/python-ci-gitlab/badges/master/pipeline.svg)](https://gitlab.com/tnt_boom/python-ci-gitlab/commits/master) 
- 點擊 `Settings` -> `CI/CD` -> 右邊 `General pipelines` 請找一下 `Pipeline status` 和 `Coverage report`, 將 Markdown 語法的文字複製並貼到 `README.md` 的第一行就可以了
- 如果想要在專案一開頭就可以看到, 則是左邊 `Settings` -> `General` , 然後右邊的 `Badges`

| | Link | Badge image URL |     
|--|--|--|
| pipeline staus | `https://gitlab.com/%{project_path}/commits/%{default_branch}` | `https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg` |
| coverage staus | `https://gitlab.com/%{project_path}/commits/%{default_branch}` | `https://gitlab.com/%{project_path}/badges/%{default_branch}/coverage.svg` |

# Security Scan
- 其實可以直接使用 [SAST](https://docs.gitlab.com/ee/ci/examples/), 不過要有 GitLab Ultimate 才可以
- 如果跟筆者一樣窮困, 可以使用 `bandit`, 請參考.gitlab-ci.yml 的 `scan` 這個stage
- 然後到 `CI/CD` -> `Jobs` 點擊剛執行完的 `security_scan_stage` 看看執行出來的 console output 即可

# Module 上傳到 Nexus
- 如果所寫的是屬於 Python module, 則是需要上傳到 Nexus (行外 Nexus Server: http://52.193.209.98:8081)
##  設定步驟
- I. 在 `.gitlab-ci.yml` 找到 `stages` 然後把 `- upload_stage` 前面註解拿掉
- II. 在 `.gitlab-ci.yml` 找到 `upload:` 並把從 `upload` 到最後一行的註解都拿掉
- II. 在 gitlab 網頁, 點擊 `Settings` -> `CD/CD` -> 右邊點選 `Varabiles` 填上下面的值, 最後 `Marked` 都要點選 (預設沒點選) 
    - 關於 `NEXUS_PASSWORD` 要找 [Fu-Ming Tsai](@sary357)

|Key | Value |     
|--|--|
| NEXUS_PASSWORD | ************ |
| NEXUS_USERNAME | cicd |

- IV. 當每次下 git push 之後, 可以點選 `CI/CD` -> `Jobs` , 應該會看到一個 stage = upload_stage 的 Job, 點進去就可以看到 job status 和執行結果

# P.S.
- 因為這邊假設是用來計算錢, 通常錢在 python 會用 decimal 計算, 而不是直接用 float or double 計算, 請注意, 如果自己程式不是計算錢, 在程式就不需要用到 decimal
- 本專案請不要修改 master branch, 請在 dev branch 新增 feature branch 修改, 修改完先進 dev branch, 再送 `Merge Requests` 並將 `Assignee` 指定給 [Fu-Ming Tsai](@sary357)
