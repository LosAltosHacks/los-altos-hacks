<?php

$state = urlencode($_GET['state']);
$city = urlencode($_GET['city']);
$zipcode = urlencode($_GET['zipcode']);
$name = urlencode($_GET['name']);


$ch = curl_init();
// curl_setopt($ch, CURLOPT_URL, "https://nces.ed.gov/ccd/schoolsearch/school_list.asp?Search=1&InstName=$name&HiGrade=13");
curl_setopt($ch, CURLOPT_URL, "https://nces.ed.gov/globallocator/index.asp?State=$state&city=$city&zipcode=$zipcode&miles=&itemname=$name&sortby=name&School=1&PrivSchool=1");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$school = curl_exec($ch);
curl_close($ch);

$school = preg_replace("/src/i", "", $school);
echo $school;
echo 'hi';

 ?>
