#!/bin/bash

for f in $(cat svg.lst); do
	wget http://smu-facweb.smu.ca/~s0949176/sammy/$f;
done
