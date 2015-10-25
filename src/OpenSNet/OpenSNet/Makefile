CC = gcc
CFLAGS = -g -Wall -Wimplicit-function-declaration -I /usr/local/include/

OpenSNet: main.o SNAttributes.o SNNets.o SNHeartBeat.o SNUtils.o
	$(CC) -o $@ $^ $(CFLAGS) /usr/local/lib/libmbedcrypto.a

main.o: main.c SNAttributes.h SNNets.h SNHeartBeat.h SNConstants.h
	$(CC) -o $@ $< $(CFLAGS) -c

SNAttributes.o: SNAttributes.c SNAttributes.h SNConstants.h
	$(CC) -o $@ $< $(CFLAGS) -c

SNHeartBeat.o: SNHeartBeat.c SNHeartBeat.h SNConstants.h
	$(CC) -o $@ $< $(CFLAGS) -c

SNNets.o: SNNets.c SNNets.h SNConstants.h
	$(CC) -o $@ $< $(CFLAGS) -c

SNUtils.o: SNUtils.c SNUtils.h SNConstants.h
	$(CC) -o $@ $< $(CFLAGS) -c

clean:
	rm *.o OpenSNet
