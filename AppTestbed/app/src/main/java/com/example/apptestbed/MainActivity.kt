package com.example.apptestbed

import android.content.Context
import android.content.Intent
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.Message
import java.lang.Thread
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.preference.Preference
import androidx.preference.PreferenceManager
import com.example.apptestbed.databinding.ActivityMainBinding
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {

    val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        var total = 0
        var started = false

        val hander = object : Handler(Looper.getMainLooper()){
            override fun handleMessage(msg: Message){
                val minute = String.format("%02d", total/60)
                val second = String.format("%02d", total%60)
                binding.textTimer.text = "$minute:$second"
            }
        }

        binding.buttonStart.setOnClickListener {

        }
    }
}