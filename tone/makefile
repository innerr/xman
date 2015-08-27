CXX=g++
CXXFLAGS=-Wall

all: tone

tone.o: tone.c
	$(CXX) $(CXXFLAGS) -c tone.c -o tone.o

tone: tone.o
	$(CXX) $(LDFLAGS)  tone.o -lm -o tone
