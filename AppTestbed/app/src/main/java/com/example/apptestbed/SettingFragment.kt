package com.example.apptestbed

import android.os.Bundle
import androidx.preference.PreferenceFragmentCompat
import java.time.Instant

class SettingFragment: PreferenceFragmentCompat() {
    override fun onCreatePreferences(savedInstanceState: Bundle?, rootKey: String?) {
        addPreferencesFromResource(R.xml.preferences)
    }
}