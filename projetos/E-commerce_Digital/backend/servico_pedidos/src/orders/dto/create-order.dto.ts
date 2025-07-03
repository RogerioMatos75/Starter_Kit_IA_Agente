import { IsString, IsNotEmpty } from 'class-validator';

export class CreateOrderDto {
  @IsString()
  @IsNotEmpty()
  readonly shippingAddress: string;

  // Outros campos relacionados ao pagamento (ex: token do cartão) seriam adicionados aqui
}
