#ifndef __B_LUX_V20_H
#define __B_LUX_V20_H

/*--------------------------Header file references--------------------------------*/
/**************************************************************************************************
 *                                        - ioCC2530.h -
 *
 * Header file with definitions for the Texas Instruments CC2530 low-power System-on-Chip: 
 * an 8051-based MCU with 2.4 GHz IEEE 802.15.4 RF transceiver, and up to 256 kB FLASH.
 *
 * This file supports IAR, Keil and SDCC compilers.
 *
 **************************************************************************************************
 */
#include <iocc2530.h>

/*-----------------------------Structure is defined---------------------------------*/

/*-----------------------------Macro definition---------------------------------*/
//Data type definitions
#define   uint16    unsigned int
#define   uint8     unsigned char
#define   fint32    float
#define   uint32    unsigned long

//Pin Definitions
#define B_LUX_SCL0_O P1DIR |= 0x40
#define B_LUX_SCL0_H P1_6 = 1
#define B_LUX_SCL0_L P1_6 = 0

#define B_LUX_SDA0_O P1DIR |= 0x08
#define B_LUX_SDA0_H P1_3 = 1
#define B_LUX_SDA0_L P1_3 = 0

#define B_LUX_SDA0_I P1DIR &= ~0x08
#define B_LUX_SDA0_DAT  P1_3

#define	B_LUX_SlaveAddress	  0x46 //The device is defined in the IIC bus slave address, according to the address pins of different modifications ALT ADDRESS

/*-----------------------------Function declaration-------------------------------*/
void B_LUX_delay_nms(uint16 k);
void B_LUX_Init(void);

void  B_LUX_Single_Write(uint8 REG_Address);               //Single write data
uint8 B_LUX_Single_Read(uint8 REG_Address);                //Single read the internal register data
void  B_LUX_Multiple_read(void);                           //Continuous reading internal register data
//------------------------------------
void B_LUX_Delay5us(void);
void B_LUX_Delay5ms(void);
void B_LUX_Start(void);                    //Start signal
void B_LUX_Stop(void);                     //Stop signal
void B_LUX_SendACK(uint8 ack);             //ACK response
uint8  B_LUX_RecvACK(void);                //Read ack
void B_LUX_SendByte(uint8 dat);            //IIC single byte write
uint8 B_LUX_RecvByte(void);                //IIC single byte read

uint32 B_LUX_GetLux(void);
#endif
