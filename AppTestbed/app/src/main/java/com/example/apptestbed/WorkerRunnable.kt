package com.example.apptestbed

import android.util.Log

class WorkerRunnable: Runnable {
    override fun run(){
        var i = 0
        while(i<10){
            i += 1
            Log.i("WorkerThread","$i")
        }
    }
}