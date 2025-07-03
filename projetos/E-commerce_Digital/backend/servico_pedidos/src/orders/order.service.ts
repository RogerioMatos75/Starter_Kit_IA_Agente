import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Order, OrderStatus } from './entities/order.entity';
import { OrderItem } from './entities/order-item.entity';
import { CreateOrderDto } from './dto/create-order.dto';
import { Cart } from '../cart/entities/cart.entity';

@Injectable()
export class OrderService {
  constructor(
    @InjectRepository(Order)
    private orderRepository: Repository<Order>,
    @InjectRepository(OrderItem)
    private orderItemRepository: Repository<OrderItem>,
    @InjectRepository(Cart)
    private cartRepository: Repository<Cart>,
  ) {}

  async checkout(userId: number, createOrderDto: CreateOrderDto): Promise<Order> {
    const cart = await this.cartRepository.findOne({ where: { userId }, relations: ['items'] });

    if (!cart || cart.items.length === 0) {
      throw new NotFoundException('Carrinho vazio ou não encontrado.');
    }

    // Simulação de processamento de pagamento
    const paymentSuccessful = Math.random() > 0.1; // 90% de chance de sucesso

    if (!paymentSuccessful) {
      const failedOrder = this.orderRepository.create({
        userId,
        totalAmount: 0, // Ou calcular o total do carrinho
        status: OrderStatus.PAYMENT_FAILED,
        shippingAddress: createOrderDto.shippingAddress,
      });
      await this.orderRepository.save(failedOrder);
      throw new Error('Falha no processamento do pagamento.');
    }

    // Simulação de cálculo de frete
    const shippingCost = 15.00; // Valor fixo para simulação

    const totalAmount = cart.items.reduce((sum, item) => sum + (item.quantity * 10), shippingCost); // Preço do produto fixo para simulação

    const order = this.orderRepository.create({
      userId,
      totalAmount,
      status: OrderStatus.APPROVED,
      shippingAddress: createOrderDto.shippingAddress,
    });

    const savedOrder = await this.orderRepository.save(order);

    const orderItems = cart.items.map(item =>
      this.orderItemRepository.create({
        productId: item.productId,
        quantity: item.quantity,
        price: 10, // Preço do produto fixo para simulação
        order: savedOrder,
      }),
    );

    await this.orderItemRepository.save(orderItems);

    // Limpar o carrinho após o checkout
    await this.cartRepository.remove(cart);

    return savedOrder;
  }

  async findAll(): Promise<Order[]> {
    return this.orderRepository.find({ relations: ['items'] });
  }
}