package com.example.leavemealoneapplication


import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.ConnectivityManager.NetworkCallback
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.os.Build
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.core.content.ContextCompat.startActivity
import android.app.Activity
import android.provider.Settings

@RequiresApi(Build.VERSION_CODES.LOLLIPOP)
class NetworkConnectionStateMonitor(context: Context) : NetworkCallback() {

    private var context : Context? = null
    private var networkRequest: NetworkRequest? = null
    private var connectivityManager : ConnectivityManager? = null

    init {
        this.context = context
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            this.networkRequest =
                    NetworkRequest.Builder()
                            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI).build()
        }
    }

    fun register() {
        connectivityManager = context!!.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            connectivityManager!!.registerNetworkCallback(networkRequest!!, this)
        }
    }

    fun unregister() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            connectivityManager!!.unregisterNetworkCallback(this)
        }
    }

    override fun onAvailable(network: Network) {
        super.onAvailable(network)
// Do what you need to do here
// 네트워크가 연결되었을 때 할 동작
        Toast.makeText(this.context, "WiFi available", Toast.LENGTH_SHORT).show()

    }


    override fun onLost(network: Network) {
        super.onLost(network)
// Do what you need to do here
// 네트워크 연결이 끊겼을 때 할 동작
        Toast.makeText(this.context, "WiFi lost", Toast.LENGTH_SHORT).show()
    }
}