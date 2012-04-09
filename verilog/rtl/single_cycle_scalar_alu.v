//
// Handles arithmetic operations that take one cycle to complete.
// The output is not registered.
//

module single_cycle_scalar_alu(
    input [5:0]                 operation_i,
    input [31:0]                operand1_i,
    input [31:0]                operand2_i,
    output reg[31:0]            result_o = 0);
    
    reg[6:0]                    leading_zeroes = 0;
    reg[6:0]                    trailing_zeroes = 0;
    integer                     i, j;

    wire[31:0] difference = operand1_i - operand2_i;
    wire negative = difference[31]; 
    wire overflow =  operand2_i[31] == difference[31] && operand1_i[31] != operand2_i[31];
    wire equal = difference == 0;
    
    always @*
    begin
        trailing_zeroes = 32;
        for (i = 31; i >= 0; i = i - 1)
            if (operand2_i[i])
                trailing_zeroes = i;
    end

    always @*
    begin
        leading_zeroes = 32;
        for (j = 0; j < 32; j = j + 1)
            if (operand2_i[j])
                leading_zeroes = 31 - j;
    end

    always @*
    begin
        case (operation_i)
            `OP_OR: result_o = operand1_i | operand2_i;
            `OP_AND: result_o = operand1_i & operand2_i;
            `OP_UMINUS: result_o = -operand2_i;     
            `OP_XOR: result_o = operand1_i ^ operand2_i;      
            `OP_NOT: result_o = ~operand2_i;
            `OP_IADD: result_o = operand1_i + operand2_i;      
            `OP_ISUB: result_o = difference;     
            `OP_ASR: result_o = { {32{operand1_i[31]}}, operand1_i } >> operand2_i;      
            `OP_LSR: result_o = operand1_i >> operand2_i;      
            `OP_LSL: result_o = operand2_i[31:5] == 0 ? operand1_i << operand2_i[4:0] : 0;
            `OP_CLZ: result_o = leading_zeroes;   
            `OP_CTZ: result_o = trailing_zeroes;
            `OP_COPY: result_o = operand2_i;   
            `OP_EQUAL: result_o = { {31{1'b0}}, equal };   
            `OP_NEQUAL: result_o = { {31{1'b0}}, ~equal }; 
            `OP_SIGTR: result_o = { {31{1'b0}}, (overflow ^ ~negative) & ~equal };
            `OP_SIGTE: result_o = { {31{1'b0}}, overflow ^ ~negative }; 
            `OP_SILT: result_o = { {31{1'b0}}, (overflow ^ negative) }; 
            `OP_SILTE: result_o = { {31{1'b0}}, (overflow ^ negative) | equal };
            `OP_UIGTR: result_o = { {31{1'b0}}, ~negative & ~equal };
            `OP_UIGTE: result_o = { {31{1'b0}}, ~negative };
            `OP_UILT: result_o = { {31{1'b0}}, negative };
            `OP_UILTE: result_o = { {31{1'b0}}, negative | equal };
            default:   result_o = 0;	// Will happen.  We technically don't care, but make consistent for simulation.
        endcase
    end
endmodule
