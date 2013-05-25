#include<iostream>
#include<stdlib.h>
#include<string.h>
using namespace std;
void usage();
void splitData(char*,float*,int);
int validity(char*,int);
class Router
{
	private :  float file_size;//File size in MB
		   int no_of_routers;//Total number of routers betweens the ends
		   float* transmission_speeds;//Transmissions speeds in each line
		   long int line_length;//Total length of each line
		   double propagation_speed;//Average propagation_speed
		   long int no_of_packets;//Number of Packets
	public : 
		   Router(float temp_size , int temp_routers , float temp_trans_speed[] , long int temp_length , double temp_prop_speed , long int temp_packets)
		   {
		   	/*Initializing values*/
			file_size=temp_size;
			no_of_routers=temp_routers;
			transmission_speeds=new float[no_of_routers+1];	
			for(int i=0;i<=no_of_routers;i++)
				transmission_speeds[i]=temp_trans_speed[i];
			line_length=temp_length;
			propagation_speed=temp_prop_speed;	
			no_of_packets=temp_packets;
	           }

		   double computeEndToEndDelay()
		   {
			double net_transmission_time=0.0, net_propagation_time,greatest,temp_val;
			//Computing the net propagation delay
			if (propagation_speed>0)
                              net_propagation_time=(((double)line_length*1000)/(propagation_speed*100000000))*(no_of_routers+no_of_packets);
			else
                              net_propagation_time=0.0;
                        //Computing the net transmission delay
			greatest=((double)file_size*(double)8/transmission_speeds[0])/(double)no_of_packets;
			for(int i=1;i<=no_of_routers;i++)
			{
				temp_val=((double)file_size*(double)8/transmission_speeds[i])/(double)no_of_packets;
				net_transmission_time+=temp_val;
				if(greatest<temp_val)	
					greatest=temp_val;	
			}
			return net_transmission_time + net_propagation_time + (no_of_packets*greatest);//Returning the final answer
		   }
                   
};
int main(int argc, char *argv[])
{
	float temp_size=-1.0;
	int temp_routers=-1,len,c;
	float *temp_trans_speed;
	char *temp_speeds;
	long int temp_length=-1,temp_packets=-1;
	double temp_prop_speed=-1.0;	
	while((c = getopt(argc,argv,":r:p:f:l:n:t:")) != -1)
		switch(c)
		{
			case 'r':	temp_routers=atoi(optarg);
					//cout<<n:"Success r "<<optarg<<endl;
					break;
			case 'n':	temp_packets=atol(optarg);
					break;
			case 'p':	temp_prop_speed=atof(optarg);
					//cout<<" Success p "<<optarg<<endl;
					break;
			case 'f':	temp_size=atof(optarg);
					//cout<<"Success f ";
					break;
			case 'l':	temp_length=atol(optarg);
					//cout<<"Success l ";
					break;
			case 't':       temp_speeds=optarg;
					//len=strlen(temp_speeds);
					//cout<<"Success t = "<<temp_speeds;
					break;
			default:	usage();//Displaying the usage if the user input is wrong
		}
	if(temp_size<0 && temp_routers<0 && temp_length<0 && temp_prop_speed<0 && temp_packets<0)
		usage();//Validating the passed parameters
	else if(!validity(temp_speeds,temp_routers))
		usage();//Validating the transmission speeds on each line
	else
	{	
		temp_trans_speed=new float[temp_routers+1];//Number of lines = Number of routers + 1
		splitData(temp_speeds,temp_trans_speed,temp_routers);//Obtaining individual transmission speeds
		cout<<"\nFile Size = "<<temp_size<<"MB\n"<<"Number of Routers = "<< temp_routers<<"\nLength of each link = "<<temp_length<<" Km\nPropagation Speed = "<<temp_prop_speed<<" X 10^8 m/s\nNumber of Packets = "<<temp_packets<<endl;//Displaying the input data before processing
		for(int i=0;i<=temp_routers;i++) 
			cout<<"Transmission Speed in link"<<i+1<<" = "<<temp_trans_speed[i]<<endl;
		Router obj(temp_size,temp_routers,temp_trans_speed,temp_length,temp_prop_speed,temp_packets);
		cout<<"\nThe end-to-end delay is "<<obj.computeEndToEndDelay()<<"s\n";
	}
	return 0;
}
void splitData(char *str,float *ar, int n)
{
	char *temp,*temp2;
	temp2=new char[n];
	strcpy(temp2,str);
	temp=strtok(str," \t");
	int i=0;
	ar[i++]=atof(temp);
	while(temp!=NULL)
	{	
		ar[i++]=atof(temp);
		temp=strtok(NULL," \t");
	}
}
int validity(char *str,int n)
{
	char *temp,*temp2;
	temp2=new char[n];
	strcpy(temp2,str);
        temp=strtok(temp2," \t");
        int i=0;
        while(temp!=NULL)
        {
                i++;
                temp=strtok(NULL," \t");
        }
	if((n+1)==i)
		return 1;
	else
		return 0;
}
void usage()
{
	cout<<"Invalid Input\n";
	exit(0);
}
