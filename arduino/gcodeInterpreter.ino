#define MAX_BUF 64
#define STEPS_PER_TURN 400



typedef struct {
  long delta;
  long absdelta;
  int dir;
  long over;
} Axis;

Adafruit_MotorShield AFMS0 = Adafruit_MotorShield(0x61);
Adafruit_MotorShield AFMS1 = Adafruit_MotorShield(0x60);

Adafruit_StepperMotor *m[4];



Axis a[4];
Axis atemp;


char buffer[MAX_BUF];
int sofar;

float px, py, pz, pe;

// speeds
float fr = 0;
long step_delay;


void feedrate(float nfr) {
  if(fr==nfr)
    return;

  step_delay = 1000000.0/nfr;
  fr=nfr;
}


void position(float npx,float npy,float npz,float npe) {
  px = npx;
  py = npy;
  pz = npz;
  pe = npe;
}

void onestep(int motor,int direction) {
  m[motor] -> onestep(direction > 0 ? FORWARD : BACKWARD, SINGLE);
}

void release() {
  int i;
  for(i=0; i<4; ++i) {
    m[i]->release();
  }
}

void line(float newx,float newy,float newz,float newe) {
  a[0].delta = newx-px;
  a[1].delta = newy-py;
  a[2].delta = newz-pz;
  a[3].delta = newe-pe;

  long i,j,maxsteps=0;

  for(i=0; i<NUM_AXIES; ++i) {
    a[i].absdelta = abs(a[i].delta);
    a[i].dir = a[i].delta > 0 ? 1:-1;
    if(maxsteps < a[i].absdelta)
      maxsteps = a[i].absdelta;
  }

  for(i=0; i<NUM_AXIES; ++i) {
    a[i].over=maxsteps/2;
  }

  for(i=0; i<maxsteps; ++i) {
    for(j=0; j<NUM_AXIES; ++j) {
      a[j].over += a[j].absdelta;
      if(a[j].over >= maxsteps) {
        a[j].over -= maxsteps;
        onestep(j,a[j].dir);
      }
    }
    pause(step_delay);
  }

  position(newx,newy,newz,newe);
}

float parsenumber(char code,float val) {
  char *ptr=buffer;
  while(ptr && *ptr && ptr<buffer+sofar) {
    if(*ptr==code) {
      return atof(ptr+1);
    }
    ptr=strchr(ptr,' ')+1;
  }
  return val;
}

void analysiereBefehl() {
  cmd = parsenumber('G',-1);

  switch(cmd) {
    case  1:
      line(
            parsenumber('X',px),
            parsenumber('Y',py),
            parsenumber('Z',pz),
            parsenumber('E',pe)
          );
      break;

    case 92:
      position(
                parsenumber('X',0),
                parsenumber('Y',0),
                parsenumber('Z',0),
                parsenumber('E',0)
              );
      break;

    default:
      break;
  }
}

void ready() {
  sofar = 0;
}


void setup() {
  Serial.begin(115200);

  AFMS0.begin(); // Start the shields
  AFMS1.begin();

  m[0] = AFMS0.getStepper(STEPS_PER_TURN, 1);
  m[1] = AFMS0.getStepper(STEPS_PER_TURN, 2);
  m[2] = AFMS1.getStepper(STEPS_PER_TURN, 1);
  m[3] = AFMS1.getStepper(STEPS_PER_TURN, 2);

  position(0,0,0,0);
  feedrate(200);
  ready();
}

void loop() {
  while(Serial.available() > 0) {
    char c = Serial.read();

    if(sofar<MAX_BUF-1)
      buffer[sofar++]=c;
    if(c=='\n') {
      buffer[sofar]=0;
      analysiereBefehl();
      ready();
    }
  }
}
