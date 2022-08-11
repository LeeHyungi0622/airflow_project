# **Apache Airflow를 활용한 Fast API 호출을 통해 데이터 수집**

## **Overview**

이번 프로젝트에서는 


## **Dataset**

프로젝트에서 사용하게 될 데이터는 Naver 및 Kakao에서 제공되는 Open API의 검색 엔진을 활용하여 수집하였습니다. 데이터 수집은 Apache Airflow를 통해 정기적으로 데이터 수집 및 데이터베이스에 적재를 하며, 적재된 데이터는 별도의 Apache Airflow에 작성한 DAG를 통해 SQL query 처리를 하고, 별도의 데이터로 가공해서 데이터베이스에 적재합니다. 

## **Objective**

이번 프로젝트를 통해 Apache Airflow를 활용하여 DAG를 작성하고, 데이터 수집과 변환, 그리고 적재의 과정을 Operator를 사용하여 세부 Task로 분류하여 작성하는 연습을 할 것입니다. 그리고 Fast API로 작성한 어플리케이션을 Docker로 컨테이너화하여, API request를 Apache Airflow를 통해 할 수 있도록 구성해 볼 것입니다. 


### **[ 관련 데이터 수집 및 적재]**

- 

<br/>

## **Data Architecture**

![Example architecture image](assets/)

### **(1) Apache Airflow를 선택한 이유**

이번 프로젝트에서 docker를 사용하여, 로컬 환경에 Apache Airflow를 구성한 이유는  

### **(2) API 어플리케이션 개발시, Fast API 프레임워크를 선택한 이유 **


## **Data Visualization**

데이터 시각화는 

<table>
    <tr>
        <th style="text-align:center">NO</th>
        <th style="text-align:center">Image</th>
        <th style="text-align:center">Description</th>
    </tr>
    <tr>
        <td>1</td>
        <td>
            <img src="assets/" alt="" />
        </td>
        <td>
            <b>[]</b><br/>
            <small></small>     
        </td>
    </tr>
</table>

## **Prerequisites**

- Docker Desktop 설치
- 코드를 실행할 IDE (VSCODE, Sublime Text 등) 설치

<br/>

## **How to Run This Project** 

1. 

2. 

3.

4.

5.

docker build -t fastapi/v1 .

docker run -p 8000:80 fastapi/v1

uvicorn api.main:app --reload

Apache Airflow Docker container 실행


## Lessons Learned

이번 프로젝트를 통해서 본래 학습 계획에 있었던 Apache Airflow의 사용에 좀 더 익숙해지는 계기가 되었던 것 같습니다. 데이터 파이프라인의 각 각의 Task를 Operator를 사용하여 작성하고, 작성한 DAG를 통해 최종적으로 Task들을 실행해보면서, 특정 시점의 Task에서 에러가 발생시 로그를 보면서 디버깅해보는 연습도 해보았습니다.
그리고 Fast API 프레임워크를 사용하여 직접 API 애플리케이션을 만들어보고, API request를 Airflow를 통해서 정기적으로 요청하여 데이터를 수집하면서, 이전에 AWS의 EventBridge 서비스를 사용했을 때 보다 좀 더 파이프라인의 Task를 세부적으로 커스텀할 수 있다고 생각했습니다.

또한 실무에서도 데이터 수집을 위해 직접 작성한 API 애플리케이션을 Airflow를 통해 정기적으로 데이터베이스에 수집되도록 해놓으면, 좀 더 효율적으로 데이터 분석가나 데이터 사이언티스트들이 업무적으로 활용할 데이터를 수집할 수 있을 것이라고 생각했습니다.

## Issue

(1) Dockerized Apache Airflow에서 DAG의 Task에서 사용할 connection에 대한 정의를 할 때 어떻게 정의해야될지 혼동이 되었습니다.

`solution)` Docker 내에서 localhost는 Docker 자체의 localhost가 되기 때문에 `host.docker.internal`로 해야 host의 localhost(127.0.0.1)로 설정할 수 있습니다. 
