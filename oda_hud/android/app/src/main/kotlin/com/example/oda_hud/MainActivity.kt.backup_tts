package com.example.oda_hud

import android.content.Intent
import android.os.Build
import android.os.Bundle
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {

    companion object {
        private const val CHANNEL = "odas/background"
    }

    override fun configureFlutterEngine(
        flutterEngine: FlutterEngine
    ) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            CHANNEL
        ).setMethodCallHandler { call, result ->

            when (call.method) {

                "startForegroundService" -> {
                    startOdaService()
                    result.success(true)
                }

                "stopForegroundService" -> {
                    stopOdaService()
                    result.success(true)
                }

                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    private fun startOdaService() {

        val intent = Intent(
            this,
            OdaForegroundService::class.java
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            ContextCompat.startForegroundService(
                this,
                intent
            )
        } else {
            startService(intent)
        }
    }

    private fun stopOdaService() {

        val intent = Intent(
            this,
            OdaForegroundService::class.java
        )

        stopService(intent)
    }
}
