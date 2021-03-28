package com.example.leavemealoneapplication

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 1. 기본 타입 배열 선언하기 - 각 기본 타입별로 10개의 빈 공간이 할당됩니다.
        var students =IntArray(10)
        var longArray = LongArray(10)
        var CharArray = CharArray(10)
        var FloatArray = FloatArray(10)
        var DoubleArray = DoubleArray(10)
        // arrayOf 함수를 사용하면 선언과 동시에 값을 입력할 수 있습니다.
        var intArray = intArrayOf(1,2,3,4,5,6,7,8,9,10)
        // intArray 변수에는 1부터 10까지의 값이 각각의 배열 공간에 저장되어 있습니다.

        // 2. 문자열 타입 배열 선언하기
        var stringArray = Array(10, {item->""})
        // arrayOf 함수로 값을 직접 입력해서 배열을 생성할 수 있습니다.
        var dayArray = arrayOf("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")

        // 3. 앞에서 선언한 students 변수에 값 넣기
        // 가. 대괄호를 사용하는 방법
        students[0] = 90
        students[1] = 91
        students[2] = 92
        students[3] = 93
        students[4] = 94
        // 나. set 함수를 사용하는 방법
        students.set(5, 95)
        students.set(6, 96)
        students.set(7, 97)
        students.set(8, 98)
    }
