import { IsString, IsNotEmpty, IsEmail } from 'class-validator';

export class SendOrderShippedDto {
  @IsEmail()
  @IsNotEmpty()
  readonly recipientEmail: string;

  @IsString()
  @IsNotEmpty()
  readonly orderNumber: string;

  @IsString()
  @IsNotEmpty()
  readonly trackingCode: string;
}
