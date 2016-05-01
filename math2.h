#ifndef MATH2_H
#define MATH2_H


static double cosd(double deg);
static double sind(double deg);
static double tand(double deg);
static double epoch();	
static double contain(double mi, double x, double ma);
static int convertRGBA2Int(int r, int g, int b, int a);
static int convertRGB2Int(int r, int g, int b);
static void convertInt2RGBA(int argb, int *r, int *g, int *b, int *a);
static double
	D2R = M_PI / 180;


static double cosd(double deg) {return cos(deg * D2R);}
static double sind(double deg) {return sin(deg * D2R);}
static double tand(double deg) {return tan(deg * D2R);}

static double epoch() {
	return time(NULL);
}	
	
static double contain(double mi, double x, double ma) {
	return (x < mi) ? mi : ((x > ma) ? ma : x);
}

static int convertRGBA2Int(int r, int g, int b, int a) {
	return (a&0x0ff) << 24 | (r&0x0ff) << 16 | (g&0x0ff) << 8 | (b&0x0ff);
}
static int convertRGB2Int(int r, int g, int b) {
	return (255&0x0ff) << 24 | (r&0x0ff) << 16 | (g&0x0ff) << 8 | (b&0x0ff);
}

static void convertInt2RGBA(int argb, int *r, int *g, int *b, int *a) {
	*r = (argb>>16) & 0xFF;
	*g = (argb>>8) & 0xFF;
	*b = (argb) & 0xFF;
	*a = (argb>>24) & 0xFF;
}


#endif