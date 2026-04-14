using UnityEngine;
using UnityEngine.UI;

public class TimeUI : MonoBehaviour
{
    public TimeController timeController;

    public void Pause()
    {
        timeController.SetScale(0);
    }

    public void Normal()
    {
        timeController.SetScale(500);
    }

    public void Fast()
    {
        timeController.SetScale(2000);
    }
}