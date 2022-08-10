
<div align="center">
  <img style="width:50%" src="https://keeper.or.kr/static/media/keeper_logo.95fc99d7fb9d9db8b162.png"/>
  <br>

  <h1>DBMigration</h1>

  <h4>DB 이관에 관련된 코드나 SQL을 모아놓는 repo입니다.</h4>

  <img src="https://img.shields.io/badge/MySQL-8-gray?logo=mysql&logoColor=4479A1&labelColor=white&style=flat-square"/> 
  <img src="https://img.shields.io/badge/Python-3.6<-gray?logo=python&logoColor=white&labelColor=3776AB&style=flat-square"/>

</div>

<br/>

### Introduction
&nbsp;&nbsp;기존 KEEPER 홈페이지는 [XpressEngine](https://www.xpressengine.com/)으로 생성된 웹사이트였습니다. DB 또한 해당 엔진으로 자동 생성 되었는데, [DB ASIS](#DB-ASIS)에서 볼 수 있듯이 테이블이 아주 많고, 복잡하고, 관계도 없습니다. 따라서 DB를 그대로 기용하기엔 불가능한 환경임을 고려, [새 DB](#DB-TOBE)를 설계하게 되었고, 이에 기존의 데이터를 이관하게 되었습니다.

### Features
[Modules description](./FEATURE.md)

### How to use (Linux)

```bash
git clone https://github.com/KEEPER31337/Homepage-DBMigration.git

cd Homepage-DBMigration

# We recommend read comments of below script before execute it... 
./script/migrate_keeper_db.sh
```

### Required Python package
[requirements.txt](./requirements.txt)  

<a href="https://pypi.org/project/setuptools/"><img src="https://img.shields.io/badge/-setuptools-336790" /></a>
<a href="https://pypi.org/project/PyMySQL/"><img src="https://img.shields.io/badge/-PyMySQL-ED8B00" /></a>
<a href="https://lxml.de/"><img src="https://img.shields.io/badge/-lxml-60A600" /></a>
<a href="https://pypi.org/project/markdownify/"><img src="https://img.shields.io/badge/-markdownify-FFE6FF" /></a>
<a href="https://pypi.org/project/multipledispatch/"><img src="https://img.shields.io/badge/-multipledispatch-F2C63E" /></a>

### DB ASIS
![asis](./img/keeper_db_asis.png)

### DB TOBE
- 20220610 UPDATED
![tobe](./img/keeper_db_tobe_20220610.png)
