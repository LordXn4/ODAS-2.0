package com.example.oda_hud

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder

class OdaForegroundService : Service() {

    companion object {
        const val CHANNEL_ID = "odas_voice_channel"
        const val NOTIFICATION_ID = 1001
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(
        intent: Intent?,
        flags: Int,
        startId: Int
    ): Int {

        val notification = createNotification()

        startForeground(
            NOTIFICATION_ID,
            notification
        )

        return START_STICKY
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {

            val channel = NotificationChannel(
                CHANNEL_ID,
                "ODAS — Assistente de voz",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description =
                    "Mantém o serviço de voz do ODAS ativo."
                setShowBadge(false)
            }

            val manager =
                getSystemService(NotificationManager::class.java)

            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {

        return Notification.Builder(
            this,
            CHANNEL_ID
        )
            .setContentTitle("ODAS ativo")
            .setContentText(
                "Assistente de voz em segundo plano"
            )
            .setSmallIcon(
                android.R.drawable.ic_btn_speak_now
            )
            .setOngoing(true)
            .build()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
