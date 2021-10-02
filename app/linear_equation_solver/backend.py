from sympy import Matrix
from sympy import simplify

#An object of RowOpSeq consists of a sequence of matrices connected by elementary row operations 
class RowOpSeq:
    #Initialize an object with a single matrix
    def __init__(self,A):
        assert type(A)==Matrix
        self.mat_seq=[A]
        self.row_op_seq=[]
        
    #Undo the last step of row operation
    def undo(self):
        self.mat_seq.pop() #pop() remove last item from a list
        self.row_op_seq.pop()
        
    #Add one more step to the sequence of row operations
    #row_op can be
    #(1) {"op":"n->n+km","k":k,"row":n,"row2":m}
    #(2) {"op":"n<->m","row1":n,"row2":m}
    #(3) {"op":"n->kn","k":k,"row":n}
    def add_step(self,row_op):
        self.row_op_seq+=[row_op]
        self.mat_seq+=[simplify(self.mat_seq[-1].elementary_row_op(**row_op))]
        

def find_RREF(A):
    #Let m=number of rows of A, n=number of columns of A
    m=A.shape[0]
    n=A.shape[1]

    #Initialize result to be the row operation sequence
    result=RowOpSeq(A)

    #horizontal pivot position in each row, originally all set to be -1
    hori_pvt_pos=[-1]*m

    #prev_pvt_row indicates the PREVIOUS pivot row during each elimination step,
    #initially set to be -1
    prev_pvt_row=-1

    #reduction of each column, including the last column
    #(column indexed by j=0,...,n-1)
    for j in range(n):
        #Let k be the smallest integer such that prev_pvt_row<=k<=m-1 and
        # CURRENT VALUE of result.mat_seq[-1][k,j]!=0
        k=prev_pvt_row+1
        while (k<=m-1 and result.mat_seq[-1][k,j]==0):
            k+=1

        #The reduction begins if the jth column is not all zeros below previous pivot
        if k!=m:
            #swap (prev_pvt_row+1)st and kth row if needed
            if prev_pvt_row+1!=k:
                result.add_step({"op":"n<->m","row1":prev_pvt_row+1,"row2":k})

            #normalize pivot entry
            if result.mat_seq[-1][prev_pvt_row+1,j]!=1:                    
                result.add_step({"op":"n->kn","row":prev_pvt_row+1,
                                    "k":1/result.mat_seq[-1][prev_pvt_row+1,j]})

            #Eliminate entries below pivot
            for i in range(prev_pvt_row+2,m):
                if result.mat_seq[-1][i,j]!=0:
                    result.add_step({"op":"n->n+km","k":-result.mat_seq[-1][i,j],\
                                        "row":i,"row2":prev_pvt_row+1})

            #update prev_pvt_row and hori_pvt_pos
            prev_pvt_row+=1
            hori_pvt_pos[prev_pvt_row]=j

    #elimination of entries above pivots
    for i in range(1,prev_pvt_row+1): #i runs through pivot rows (except the 0th one)
        for k in reversed(range(i)): #k runs through all entries above the ith row pivot
            if result.mat_seq[-1][k,hori_pvt_pos[i]]!=0:
                result.add_step({"op":"n->n+km",\
                                    "k":-result.mat_seq[-1][k,hori_pvt_pos[i]],\
                                    "row":k,"row2":i})

    #return the result
    return result


#from input_matrix import A