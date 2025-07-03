import { IsString, IsNotEmpty, IsEmail, IsNumber } from 'class-validator';

export class SendOrderConfirmationDto {
  @IsEmail()
  @IsNotEmpty()
  readonly recipientEmail: string;

  @IsString()
  @IsNotEmpty()
  readonly orderNumber: string;

  @IsString()
  @IsNotEmpty()
  readonly itemsSummary: string;

  @IsNumber()
  @IsNotEmpty()
  readonly totalAmount: number;
}
