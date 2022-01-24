#!/usr/bin/env bash

printf '\nList all processes\n\n' && sleep 2
curl --request GET \
  --url http://pygeoapi-testing.gispocoding.fi/processes/

printf '\n\nHello world\n\n' && sleep 2
curl --request POST \
  --url http://pygeoapi-testing.gispocoding.fi/processes/hello-world/execution \
  --header 'Content-Type: application/json' \
  --data '{
	"inputs": {
		"name": "miglu",
		"message": "custom message"
	}
}'

printf '\n\nLake exterior ring generator\n\n' && sleep 2
curl --request POST \
  --url http://pygeoapi-testing.gispocoding.fi/processes/exterior/execution \
  --header 'Content-Type: application/json' \
  --data '{
	"inputs": {
		"name": "Haukkalampi"
	}
}'

printf '\n\nRaster value picker\n\n' && sleep 2
curl --request POST \
  --url http://pygeoapi-testing.gispocoding.fi/processes/rasterval/execution \
  --header 'Content-Type: application/json' \
  --data '{
	"inputs": {
		"x": 389500,
		"y": 7216500
	}
}'

printf '\n\nLinestring reprojection\n\n' && sleep 2
curl --request POST \
  --url http://pygeoapi-testing.gispocoding.fi/processes/reproj/execution \
  --header 'Content-Type: application/json' \
  --data '{
	"inputs": {
		"geom": "LINESTRING(24.21442946538139 62.31909919027754,24.21445236824193 62.31907558605488,24.214485632246184 62.31907686361416,24.214530686826535 62.31909697065056,24.214592895052927 62.3190988463126,24.214614372829203 62.31907457576479,24.214580673114437 62.31903359716983,24.2145586974681 62.3190040364018,24.214509238483522 62.31897520021347,24.21442079957194 62.31895385525646,24.21435561967087 62.31894591983461,24.214309124022243 62.318924490411796,24.21422085107614 62.31892199330515,24.214184804694362 62.31893283078264,24.214127417083716 62.318979384791724,24.214106200925222 62.31902855019058,24.21413713275991 62.319085021610036,24.214141855299562 62.31912470982066,24.21410036461684 62.31917055853935,24.214051672768175 62.31921911023798,24.21400585136097 62.31926564458,24.214002016390136 62.31931746684975,24.214042846329797 62.31935170817022,24.214112596515555 62.31938451723752,24.214177869752845 62.319401876958416,24.21421394771698 62.31939508209788,24.21423970031753 62.31936406184279,24.214304598888695 62.319347110975386,24.214375264188455 62.319322721645705,24.21440533196011 62.31929305435204,24.214414991217787 62.31924525608602,24.21442476450236 62.3192095681089,24.214427250118646 62.31916918007517,24.21444575885718 62.31913819422728,24.21442946538139 62.31909919027754)",
		"in_crs": 4326,
		"out_crs": 3067
	}
}'

printf '\n\nLake exterior ring generator as async process\n\n' && sleep 2
curl --request POST \
  --url http://pygeoapi-testing.gispocoding.fi/processes/exterior/execution \
  --header 'Content-Type: application/json' \
  --data '{
	"mode": "async",
	"inputs": {
		"name": "Haukkalampi"
	}
}
'

printf '\n\nGet status of lake exterior ring process jobs\n\n' && sleep 2
curl --request GET \
  --url http://pygeoapi-testing.gispocoding.fi/processes/exterior/jobs \
  --header 'Content-Type: application/json'

printf '\n\nGet results of async job by id\n\n' && sleep 2
curl --request GET \
  --url 'http://pygeoapi-testing.gispocoding.fi/processes/exterior/jobs/9da16186-7cfa-11ec-b73d-0242c0a85003/results?f=json' \
  --header 'Content-Type: application/json'
