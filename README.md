# Rmoney_app

1. Run application locally:-

   a. install docker engine by following steps in below link:- <br />
      windows:- https://docs.docker.com/docker-for-windows/install/ <br />
      Linux:- https://docs.docker.com/engine/install/ubuntu/ <br />
      Mac:- https://docs.docker.com/docker-for-mac/install/ <br />
      
   b. install docker compose to run docker compose file by gollowing steps in below link:- <br />
      https://docs.docker.com/compose/install/ <br />
      
   c. download "docker-compose.yml" file in home directory of this application.
   
   d. In local system open terminal and browse to path of downloaded docker-compose file
   
   e. Now run command :- "docker-compose up"

   Note:- Before proceeding furthur please make sure docker-compose file is generating logs normally without any error message, also open url:- https://127.0.0.1:5000, if it shows "hello". It means your application is running successfully.
   
   
   
2. How to use this application:-

   a. Push stocks bhav copy in database:- <br />
      Hit the API link:- https://127.0.0.1:5000/api/v1/bhav_copy/equity/<start_date>/<end_date>  <br />
      In this API we need to mention starting date and ending date, which determine the date interval of bhav copy need to be inserted.  <br />
      The date format should be :- "DD-MM-YYYY". (No other format will be accepted)  <br />

   b. Use Command to validate data:-  <br />
      Copy the data into folder:- /CSV_files/x    (x can be "stocks", "future_options")  <br />
      files can be placed by  <br />
        "docker cp -R <source folder path> <flask contianer name>:/CSV_files/x"  <br />
      example:-  <br />
        docker cp -R /mnt/d/files rmadmin_web_1:/CSV_files/stocks  <br />
      
  
      Check if all files are present in particular date range.  <br />
        "docker exec -it rmadmin_web_1 python3 manage.py check_files_stocks <start_date> <end_date>"  <br />
        Here date format -> "DD/MM/YYYY"  <br />
        for stocks -> "check_files_stocks"  <br />
        It is generate logs of missing dates. Logs will be placed "Logs folder"  <br />
      Move log folder to desired system path  <br />
        docker cp -R <flask contianer name>:/Logs <destination path>  <br />
      example:-  <br />
        docker exec -it rmadmin_web_1 python3 manage.py check_files_stocks 01/01/2020 31/12/2020  <br />
      
  
      Check Data integrity of files in data range:-  <br />
        "docker exec -it rmadmin_web_1 python3 manage.py check_integrity_stocks <start_date> <end_date>"  <br />
        Here date format -> "DD/MM/YYYY"  <br />
        for stocks -> "check_integrity_stocks"  <br />
      Move log folder to desired system path  <br />
        docker cp -R <flask contianer name>:/Logs <destination path>  <br />
      example:-  <br />
        "docker exec -it rmadmin_web_1 python3 manage.py check_integrity_stocks 01/01/2020 31/12/2020"  <br />
   
  
      
   
