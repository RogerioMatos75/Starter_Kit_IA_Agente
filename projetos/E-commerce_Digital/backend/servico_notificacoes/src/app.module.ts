import { Module } from '@nestjs/common';
import { NotificationsModule } from './notifications/notifications.module';

@Module({
  imports: [NotificationsModule],
  controllers: [],
  providers: [],
})
export class AppModule {}
