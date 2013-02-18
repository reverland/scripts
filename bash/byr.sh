#! /usr/bin/expect

spawn luit -encoding gbk telnet bbs.byr.cn

expect ":" {
	send "username\n"

	send "password\n"
      }
interact {
	timeout 30 {send "\014"}
      }
