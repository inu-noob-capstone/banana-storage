package com.example.leavemealoneapplication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.core.widget.addTextChangedListener
import com.example.leavemealoneapplication.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        val moistureIntent = Intent(this, MoistureManagement::class.java)
        val lightIntent = Intent(this, LightManagement::class.java)

        binding.mainMoisture.setOnClickListener { startActivity(moistureIntent) }
        binding.mainLight.setOnClickListener { startActivity(lightIntent) }
    }
}
