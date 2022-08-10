## DBMigration features
---
- `extra_vars_inserter`  
    기존 DB의 json 유사 format을 파싱 후, 학번 등을 새 컬럼에 삽입
    
    <details>
    <summary>해당 format</summary>
        <pre>O:8:"stdClass":5:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:11:"birthday_ui";s:10:"1998-09-24";s:21:"__profile_image_exist";s:5:"false";s:12:"phone_number";a:3:{i:0;s:3:"010";i:1;s:4:"1234";i:2;s:4:"5678";}s:13:"studentnumber";s:9:"201712345";}</pre>
    </details>
    
    [issue #1](https://github.com/KEEPER31337/Homepage-DBMigration/issues/1) [#3](https://github.com/KEEPER31337/Homepage-DBMigration/issues/3)

- `parent_puller`  
    새 홈페이지의 댓글 정책이 대댓글의 깊이를 1로 제한함에 따라, 재귀를 이용하여 구 DB의 대댓글 깊이를 1로 조정  
    [issue #5](https://github.com/KEEPER31337/Homepage-DBMigration/issues/5)

- `group_seperator`  
    통합되어 있는 회원 직위, 등급, 유형 정보들을 각각의 테이블로 분리하고, 1:n, n:m으로 세분화함. 이에, 달라진 테이블 구조에 맞춰 데이터 이관  
    [issue #6](https://github.com/KEEPER31337/Homepage-DBMigration/issues/6)

- `html_content_cleaner`  
    게시글 글자 수 정책에 따라 불필요한 html attribute 제거 혹은 markdown으로 변형  
    [issue #7](https://github.com/KEEPER31337/Homepage-DBMigration/issues/7)

- `data_migrator`  
    별도의 데이터 조작이 필요없는 테이블들을 새 테이블과 column 1:1 매칭을 통해 SELECT - INSERT로 이관  
    [issue #8](https://github.com/KEEPER31337/Homepage-DBMigration/issues/8)

- `category_mapper`  
    게시판 제목, 부모 게시판 id 등의 정보가 `xe_modules`, `xe_menu_item`로 흩어져 있어, 통합된 테이블 생성  
    [issue #10](https://github.com/KEEPER31337/Homepage-DBMigration/issues/10)

- `category_controller`  
    새 홈페이지 기획에 맞게 게시판 통폐합
    
- `library_migrator`  
    바뀐 테이블 구조에 맞게 도서, 기자재 데이터 이관  
    [issue #12](https://github.com/KEEPER31337/Homepage-DBMigration/issues/12) [#13](https://github.com/KEEPER31337/Homepage-DBMigration/issues/13)

- `category_transferer`  
    게시판이 통폐합 되면서 기존의 게시물도 맞는 category를 배정해준다. 단, 원 출처가 되는 게시판명을 게시물 제목 앞에 대괄호와 함께 붙여준다.  
    [issue #22](https://github.com/KEEPER31337/Homepage-DBMigration/issues/22)

- ~~`password_spliter`~~  
    비밀번호를 그대로 쓰기로 하면서 deprecated  
    [issue #16](https://github.com/KEEPER31337/Homepage-DBMigration/issues/16)
