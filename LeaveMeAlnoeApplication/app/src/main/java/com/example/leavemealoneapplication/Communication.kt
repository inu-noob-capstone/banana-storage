package com.example.leavemealoneapplication

import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity

class Communication : AppCompatActivity() {

    //lateinit var networkConnectionStateMonitor: NetworkConnectionStateMonitor
    lateinit var button: Button

    lateinit var networkConnectionStateMonitor: NetworkConnectionStateMonitor

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_communication)

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            networkConnectionStateMonitor = NetworkConnectionStateMonitor(this)
        }
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            networkConnectionStateMonitor.register()
        }

        button = findViewById(R.id.communcationBtn)
        button.setOnClickListener(listener)

        var WiFiConnetion01: ImageView

        WiFiConnetion01 = findViewById(R.id.connected)

        var isWiFi = isWiFiAvailable(this)

        if(isWiFi){
            Log.d("WiFI", "WiFi On")
            WiFiConnetion01.setImageResource(R.drawable.connected)
        }
        else{
            Log.d("WiFI", "WiFi Off")
            WiFiConnetion01.setImageResource(R.drawable.unconnected)
        }
    }

    val listener = View.OnClickListener { view ->
        when(view.getId()){
            R.id.communcationBtn -> {
                startActivity(Intent(Settings.ACTION_WIFI_SETTINGS))
            }
        }
    }

    override fun onRestart() {
        super.onRestart()
        var WiFiConnection02: ImageView
        WiFiConnection02 = findViewById(R.id.connected)

        var isWiFi = isWiFiAvailable(this)

        if(isWiFi){
            Log.d("WiFI", "WiFi On")
            WiFiConnection02.setImageResource(R.drawable.connected)
        }
        else{
            Log.d("WiFI", "WiFi Off")
            WiFiConnection02.setImageResource(R.drawable.unconnected)
        }
    }
}




fun isWiFiAvailable(context: Context?) :Boolean {
    if (context == null) return false
    val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        val capabilities = connectivityManager.getNetworkCapabilities(connectivityManager.activeNetwork)
        if (capabilities != null) {
            if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI))
                return true
        }
    }
    return false
}


