//***************************************
// B_LUX_V20 Acquisition Program
//****************************************
#include  <math.h>    //Keil library  
#include  <stdio.h>   //Keil library
#include "B_LUX_V20.h"

uint8    BUF_0[8];                       //Receive data buffer      	
uint16   dis_data_0;                     //Variable

/*---------------------------------------------------------------------
 Description: Delay nanosecond different working environment, the need to adjust this function
 Parameters: None	
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_delay_nms(uint16 k)	
{						
  uint16 i,j;				
  for(i=0;i<k;i++)
  {			
    for(j=0;j<6000;j++)			
    {
      ;
    }
  }						
}					

/*---------------------------------------------------------------------
 Description: 5 microsecond delay different working environment, the need to adjust this function
 Parameters: None	
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Delay5us()
{
  uint8 n = 50;
  
  while (n--);
}

/*---------------------------------------------------------------------
 Description: 5 millisecond latency different working environment, you need to adjust this function
 Parameters: None	
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Delay5ms()
{
  uint16 n = 50000;
  
  while (n--);
}

/*---------------------------------------------------------------------
 Description: Start signal
 Parameters: None	
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Start()
{
  B_LUX_SDA0_H;                         //Pulled the data lines
  B_LUX_SCL0_H;                         //Pulled clock line
  B_LUX_Delay5us();                     //Delay
  B_LUX_SDA0_L;                         //Falling edge
  B_LUX_Delay5us();                     //Delay
  B_LUX_SCL0_L;                         //Low clock line
}

/*---------------------------------------------------------------------
 Description: Stop signal
 Parameters: None	
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Stop()
{
  B_LUX_SDA0_L;                         //Pulled the data lines
  B_LUX_SCL0_H;                         //Pulled clock line
  B_LUX_Delay5us();                     //Delay
  B_LUX_SDA0_H;                         //Rising edge
  B_LUX_Delay5us();                     //Delay
  B_LUX_SCL0_L;
  B_LUX_Delay5us();
}

/*---------------------------------------------------------------------
 Description: Sends a response signal
 Parameters: ack - Answer signal(0:ACK 1:NAK)
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_SendACK(uint8 ack)
{
  if (ack&0x01)	B_LUX_SDA0_H;		//Write a response signal
  else	B_LUX30_SDA0_L;
  
  B_LUX30_SCL0_H;                         //Pulled clock line
  B_LUX30_Delay5us();                     //Delay
  B_LUX30_SCL0_L;                         //Low clock line
  B_LUX30_SDA0_H;
  B_LUX30_Delay5us();                     //Delay
}

/*---------------------------------------------------------------------
 Description: Receiving a response signal
 Parameters: None
 Function Returns: Returns response signal
 ---------------------------------------------------------------------*/
uint8 B_LUX_RecvACK()
{
  uint8 CY = 0x00;
  B_LUX_SDA0_H;
  
  B_LUX_SDA0_I;
  
  B_LUX30_SCL0_H;                         //Pulled clock line
  B_LUX30_Delay5us();                     //Delay
  
  
  CY |= B_LUX30_SDA0_DAT;                 //Read answer signal
  
  B_LUX30_Delay5us();                     //Delay
  
  B_LUX30_SCL0_L;                         //Low clock line
  
  B_LUX_SDA0_O;
  
  return CY;
}

/*---------------------------------------------------------------------
 Description: Send a byte of data to the IIC bus
 Parameters: dat - Write Bytes
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_SendByte(uint8 dat)
{
  uint8 i;
  
  for (i=0; i<8; i++)         			//count 8
  {
    if (dat&0x80)	B_LUX_SDA0_H;
    else	B_LUX30_SDA0_L;                   //Send data port
    
    B_LUX30_Delay5us();             		//Delay
    B_LUX30_SCL0_H;                		//Pulled clock line
    B_LUX30_Delay5us();             		//Delay
    B_LUX30_SCL0_L;                		//Low clock line
    B_LUX30_Delay5us();             		//Delay
    dat <<= 1;              			//MSB shifted out data
  }
  
  B_LUX_RecvACK();
}

/*---------------------------------------------------------------------
 Description: Receiving a byte of data from the IIC bus
 Parameters: None
 Function Returns: Bytes Received
 ---------------------------------------------------------------------*/
uint8 B_LUX_RecvByte()
{
  uint8 i;
  uint8 dat = 0;
  B_LUX_SDA0_I;
  
  B_LUX_SDA0_H;                  //Enable internal pull, ready to read data,
  for (i=0; i<8; i++)         	//count 8
  {
    B_LUX30_SCL0_H;                       //Pulled clock line
    B_LUX30_Delay5us();             	//Delay
    dat |= B_LUX30_SDA0_DAT;              //Read Data               
    B_LUX30_SCL0_L;                       //Low clock line
    B_LUX30_Delay5us();             	//Delay
    
    dat <<= 1;	
  }
  B_LUX_SDA0_O;
  
  return dat;
}

/*---------------------------------------------------------------------
 Description: Write BH1750
 Parameters: REG_Address - Register Address
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Single_Write(uint8 REG_Address)
{
  B_LUX_Start();                  //Start signal
  B_LUX_SendByte(B_LUX_SlaveAddress);   //Send device address + write signal
  B_LUX_SendByte(REG_Address);    //Internal register address 
  //  BH1750_SendByte(REG_data);       //Internal register data 
  B_LUX_Stop();                   //Sending a stop signal
}

/*---------------------------------------------------------------------
 Description: Read B_LUX30
 Parameters: None
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Multiple_read(void)
{   
  uint8 i;	
  B_LUX_Start();                          //Start signal
  B_LUX_SendByte(B_LUX_SlaveAddress+1);         //Send device address + read signal
  
  for (i=0; i<3; i++)                        //6 continuous read address data stored in BUF
  {
    BUF_0[i] = B_LUX_RecvByte();          //BUF[0] data stored in the address 0x32
    if (i == 3)
    {
      
      B_LUX_SendACK(1);                   //NOACK need to return to the last data
    }
    else
    {		
      B_LUX_SendACK(0);                   //ACK responses
    }
  }
  
  B_LUX_Stop();                           //Stop signal
  B_LUX_Delay5ms();
}

/*---------------------------------------------------------------------
 Description: Light sensor initialization
 Parameters: None
 Function Returns: None
 ---------------------------------------------------------------------*/
void B_LUX_Init()
{
  
  P1SEL &= ~(0x48);
  
  B_LUX_SCL0_O;
  B_LUX_SDA0_O;
  
  B_LUX_delay_nms(100);	    //Delay 100ms
  
  B_LUX_Single_Write(0x01); 
  
}

/*---------------------------------------------------------------------
 Description: Light read function
 Parameters: None
 Function Returns: Returns lighting value
 ---------------------------------------------------------------------*/
uint32 B_LUX_GetLux()
{  
  fint32 temp;
  B_LUX_Single_Write(0x01);   // power on
  B_LUX_Single_Write(0x10);   // H- resolution mode 
  
  B_LUX_delay_nms(180);       //Delay 180ms
  
  B_LUX_Multiple_read();      //Continuous read data stored in the BUF
  
  B_LUX_Single_Write(0x00);   // power off
  
  dis_data_0=BUF_0[0];
  dis_data_0=(dis_data_0<<8)+BUF_0[1];//Synthetic data, namely light data
  
  temp=(float)dis_data_0/1.2;
  return (uint32)(temp*1.4);
} 

