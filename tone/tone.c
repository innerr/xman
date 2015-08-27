#pragma pack(1)

#include <stdio.h>
#include <string.h>

typedef unsigned short WORD;
typedef unsigned long DWORD;

typedef struct
{
	char  vFileHead1[4];
	int   nFileLength;
	char  vFileHead2[8];
	int   nReserve;
	WORD  wFormatTag;
	WORD  nChannels;
	DWORD nSamplesPerSec;
	DWORD nAvgBytesPerSec;
	WORD  nBlockAlign;
	WORD  wBitsPerSample;
} Header;

int WaveLoad(const char* strWaveName, short*& pData, Header* pHeader)
{
	FILE* file = fopen(strWaveName, "rb");
	if (file == NULL)
		return -1;

	fseek(file, 0, SEEK_END);
	int length = ftell(file);

	int nDataLength = (length - sizeof(Header)) / 2;

	fseek(file, 0, SEEK_SET);
	fread(pHeader, sizeof(Header), 1, file);

	pData = new short[nDataLength];
	memset(pData, 0, nDataLength * sizeof(short));

	fread(pData, sizeof(short), nDataLength, file);
	fclose(file);
	return nDataLength;
}

bool WaveWrite(const char* strWaveName, const Header* pHeader, const short* pData, int nDataLength)
{
	FILE* file = fopen(strWaveName, "wb");
	if (file == NULL)
		return false;
	fwrite(pHeader, sizeof(Header), 1, file);
	fwrite(pData, sizeof(short), nDataLength, file);
	fclose(file);
	return true;
}

int main()
{
	const char* strFileName = "sample.wav";
	short *pData = NULL;
	Header tagHeader;
	int nLength = WaveLoad(strFileName, pData, &tagHeader);
	printf("file: %d\nlength: %d\nrate: %d\n", tagHeader.nFileLength, nLength, int(tagHeader.nSamplesPerSec));

	const char* strFileNameLower1 = "lower_1.wav";
	Header tagHeaderLower1 = tagHeader;
	tagHeaderLower1.nSamplesPerSec /= 2;
	WaveWrite(strFileNameLower1, &tagHeaderLower1, pData, nLength);

	const char* strFileNameHigher1 = "higher_1.wav";
	Header tagHeaderHigher1 = tagHeader;
	tagHeaderHigher1.nSamplesPerSec *= 2;
	WaveWrite(strFileNameHigher1, &tagHeaderHigher1, pData, nLength);

	const char* strFileNameLower2 = "lower_2.wav";
	Header tagHeaderLower2 = tagHeader;
	short *pDataLower2 = new short[nLength * 2];
	for (int i = 0; i < nLength; i++)
	{
		pDataLower2[i * 2] = pData[i];
		pDataLower2[i * 2 + 1] = pData[i];
	}
	tagHeaderLower2.nFileLength += sizeof(short) * nLength;
	WaveWrite(strFileNameLower2, &tagHeaderLower2, pDataLower2, nLength * 2);
	delete pDataLower2;

	const char* strFileNameHigher2 = "higher_2.wav";
	Header tagHeaderHigher2 = tagHeader;
	short *pDataHigher2 = new short[nLength / 2];
	for (int i = 0; i < nLength; i++)
	{
		if ((i % 2) != 0)
			continue;
		pDataHigher2[i / 2] = pData[i];
	}
	tagHeaderHigher2.nFileLength -= sizeof(short) * (nLength - nLength / 2);
	WaveWrite(strFileNameHigher2, &tagHeaderHigher2, pDataHigher2, nLength / 2);
	delete pDataHigher2;

	delete pData;
}
