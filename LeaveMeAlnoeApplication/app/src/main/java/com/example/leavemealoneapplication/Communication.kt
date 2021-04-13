package com.example.leavemealoneapplication

import android.content.Context
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.Button
import android.widget.ImageView
import com.example.leavemealoneapplication.databinding.ActivityMainBinding

class Communication : AppCompatActivity() {

    lateinit var button: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_communication)
        button = findViewById(R.id.communcationBtn)
        button.setOnClickListener(listener)

        val imageView = ImageView(this)
        imageView.setImageResource(R.drawable.unconnected)
    }

    val listener = View.OnClickListener { view ->
        when(view.getId()){
            R.id.communcationBtn ->{
                startActivity(Intent(Settings.ACTION_WIFI_SETTINGS))

            }
        }
    }
}