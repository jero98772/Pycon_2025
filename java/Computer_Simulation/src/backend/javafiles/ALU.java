import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;
import java.util.List;
import java.util.ArrayList;

public class ALU {
    // Inputs
    short x;
    short y;

    // Control bits
    short zx;
    short nx;
    short zy;
    short ny;
    short f;
    short no;

    // Outputs
    short out1;
    short out;
    short zr;
    short ng;
    short x1;
    short x2;
    short y1;
    short y2;
    public void setInputs(short x, short y) {
        this.x = x;
        this.y = y;
    }

    public void setControlBits(short zx, short nx, short zy, short ny, short f, short no) {
        this.zx = zx;
        this.nx = nx;
        this.zy = zy;
        this.ny = ny;
        this.f = f;
        this.no = no;
    }
    public ALU() {
        /*
          x=outDReg,
          y=outAorM,
          zx=instruction[11],   // c1
          nx=instruction[10],   // c2
          zy=instruction[9],    // c3
          ny=instruction[8],    // c4
          f =instruction[7],    // c5
          no=instruction[6],    // c6
          out=outALU,
          out=outM,
          zr=isZeroOut,
          ng=isNegOut
        */
        this.x = x;
        this.y = y;
        this.zx = zx;
        this.nx = nx;
        this.zy = zy;
        this.ny = ny;
        this.f = f;
        this.no = no;
        this.out1 = out1;
        this.out =out;
        this.zr = zr;
        this.ng = ng;
        this.x1=x1;
        this.x2=x2;
        this.y1=y1;
        this.y2=y2;
    }
    public void compute() {

    this.x1 = (short) (this.zx == 1 ? 0 : this.x);           // Zero the x input
    this.x2 = (short) (this.nx == 1 ? ~this.x1 : this.x1);        // Negate the x input
    this.y1 = (short) (this.zy == 1 ? 0 : this.y);           // Zero the y input
    this.y2 = (short) (this.ny == 1 ? ~this.y1 : this.y1);        // Negate the y input

    this.out1 = (short) (this.f == 1 ? this.x2 + this.y2 : this.x2 & this.y2);  // Perform the operation
    this.out = (short) (this.no == 1 ? ~this.out1 : this.out1);             // Negate the output

    this.zr = (short) (this.out == 0 ? 1 : 0);                        // Set the zero flag
    this.ng = (short) ((short) ((this.out >> 15) & 1) == 1 ? 1 : 0);     // Set the negative flag
        System.out.println(this.y);

    }
    public short getOut() {
        return this.out;
    }

    public short getZr() {
        return this.zr;
    }

    public short getNg() {
        return this.ng;
    }
}
