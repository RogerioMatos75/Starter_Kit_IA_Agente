import { Injectable } from '@nestjs/common';
import * as nodemailer from 'nodemailer';
import { SendOrderConfirmationDto } from './dto/send-order-confirmation.dto';
import { SendOrderShippedDto } from './dto/send-order-shipped.dto';

@Injectable()
export class NotificationsService {
  private transporter;

  constructor() {
    // Configuração do Nodemailer (usando um transporte de teste para desenvolvimento)
    this.transporter = nodemailer.createTransport({
      host: 'smtp.ethereal.email',
      port: 587,
      secure: false,
      auth: {
        user: 'test.account@ethereal.email',
        pass: 'password',
      },
    });
  }

  async sendOrderConfirmation(dto: SendOrderConfirmationDto) {
    const mailOptions = {
      from: '"E-commerce Digital" <no-reply@ecommerce.com>',
      to: dto.recipientEmail,
      subject: `Confirmação do Pedido #${dto.orderNumber}`,
      html: `
        <h1>Seu pedido foi confirmado!</h1>
        <p>Número do Pedido: <strong>${dto.orderNumber}</strong></p>
        <p>Resumo dos Itens: ${dto.itemsSummary}</p>
        <p>Valor Total: R$ ${dto.totalAmount.toFixed(2)}</p>
        <p>Obrigado por sua compra!</p>
      `,
    };

    try {
      const info = await this.transporter.sendMail(mailOptions);
      console.log('E-mail de confirmação enviado: %s', info.messageId);
      console.log('URL de visualização: %s', nodemailer.getTestMessageUrl(info));
      return { success: true, messageId: info.messageId, previewUrl: nodemailer.getTestMessageUrl(info) };
    } catch (error) {
      console.error('Erro ao enviar e-mail de confirmação:', error);
      return { success: false, error: error.message };
    }
  }

  async sendOrderShipped(dto: SendOrderShippedDto) {
    const mailOptions = {
      from: '"E-commerce Digital" <no-reply@ecommerce.com>',
      to: dto.recipientEmail,
      subject: `Seu pedido #${dto.orderNumber} foi enviado!`,
      html: `
        <h1>Seu pedido foi enviado!</h1>
        <p>Número do Pedido: <strong>${dto.orderNumber}</strong></p>
        <p>Código de Rastreio: <strong>${dto.trackingCode}</strong></p>
        <p>Você pode rastrear seu pedido <a href="#">aqui</a>.</p>
        <p>Obrigado por sua compra!</p>
      `,
    };

    try {
      const info = await this.transporter.sendMail(mailOptions);
      console.log('E-mail de pedido enviado: %s', info.messageId);
      console.log('URL de visualização: %s', nodemailer.getTestMessageUrl(info));
      return { success: true, messageId: info.messageId, previewUrl: nodemailer.getTestMessageUrl(info) };
    } catch (error) {
      console.error('Erro ao enviar e-mail de pedido enviado:', error);
      return { success: false, error: error.message };
    }
  }
}
