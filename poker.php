<?php
define("COOKIE_c_user", '');
define("COOKIE_xs", '');

date_default_timezone_set('Asia/Seoul');
set_time_limit(0);

$cookie = 'xs=' . COOKIE_xs . '; c_user=' . COOKIE_c_user;

$ch = curl_init();
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_COOKIE, $cookie);
curl_setopt($ch, CURLOPT_HEADER, true);

while(1) {
	curl_setopt($ch, CURLOPT_URL, 'https://m.facebook.com/pokes');
	$data = curl_exec($ch);
	preg_match_all('/href="\/pokes\/inline\/([^"]+)">/', $data, $links);
	preg_match_all('/<a href="\/([^"]+)">([^<]+)</', $data, $names);

	foreach($links[1] as $key=>$link) {
		$link = htmlspecialchars_decode($link);
		curl_setopt($ch, CURLOPT_URL, 'https://m.facebook.com/pokes/inline/' . $link);
		$data = curl_exec($ch);
		if (strpos($names[1][$key], 'profile.php?id=') !== false) {
			preg_match('/([0-9]+)/', $names[1][$key], $match);
			$names[1][$key] = $match[1];
		}

		if (strpos($data, "sentry") !== false) {
			echo 'Failed to poke ' . $names[2][$key] . '(' . $names[1][$key] . ') - ' . date('Y-m-d H:i:s');
			sleep(600);
		} else if (strpos($data, "success") !== false) {
			echo 'Poked ' . $names[2][$key] . '(' . $names[1][$key] . ') - ' . date('Y-m-d H:i:s');
		} else {
			echo '??? ' . $names[2][$key] . '(' . $names[1][$key] . ') - ' . date('Y-m-d H:i:s');
		}
		echo "\n";
	}
}
