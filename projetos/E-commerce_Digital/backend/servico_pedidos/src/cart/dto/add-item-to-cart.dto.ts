import { IsString, IsNumber, IsNotEmpty } from 'class-validator';

export class AddItemToCartDto {
  @IsString()
  @IsNotEmpty()
  readonly productId: string;

  @IsNumber()
  @IsNotEmpty()
  readonly quantity: number;
}
