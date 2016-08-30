<?php
include("db.php");
$id = 121;
$sql = "Select speed from speedo where id=$id";
$result = $connection->query($sql);
$row = $result->fetch_assoc();
echo $row['speed'];
?>