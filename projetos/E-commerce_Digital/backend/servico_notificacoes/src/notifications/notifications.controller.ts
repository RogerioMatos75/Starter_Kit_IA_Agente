import { Controller, Post, Body } from '@nestjs/common';
import { NotificationsService } from './notifications.service';
import { SendOrderConfirmationDto } from './dto/send-order-confirmation.dto';
import { SendOrderShippedDto } from './dto/send-order-shipped.dto';

@Controller('notifications')
export class NotificationsController {
  constructor(private readonly notificationsService: NotificationsService) {}

  @Post('order-confirmation')
  sendOrderConfirmation(@Body() sendOrderConfirmationDto: SendOrderConfirmationDto) {
    return this.notificationsService.sendOrderConfirmation(sendOrderConfirmationDto);
  }

  @Post('order-shipped')
  sendOrderShipped(@Body() sendOrderShippedDto: SendOrderShippedDto) {
    return this.notificationsService.sendOrderShipped(sendOrderShippedDto);
  }
}
