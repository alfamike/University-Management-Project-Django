package eu.university;

import org.hyperledger.fabric.shim.ChaincodeBase;

public class student_cc extends ChaincodeBase {

    @Override
    public Response init(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    @Override
    public Response invoke(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    public static void main(String[] args) {
        new student_cc().start(args);
    }
    
}
