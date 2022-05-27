using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using PathCreation; 

public class BluePlayerMovement : MonoBehaviour
{

    public float speed;
    private Animator animator;
    private Rigidbody myRigidbody;
    public float FallingThreshold = -10f;
    private int currentNivell;
    private Transform myTransform;

    public GlobalVolumeManager volumeManager;
    public canvasManager canvasManager;

    public RedPlayerMovement RedPlayer; 

    public PathCreator pathCreator1;
    public PathCreator pathCreator2;
    public PathCreator pathCreator3;
    public PathCreator pathCreator4;
    public PathCreator pathCreator5;

    //Nivell 2
    public float forceGrupPunxes1;
    public float forceGrupPunxes2;
    public float forceGrupPunxes3;
    public float forceGirador1; 
    public float forceGirador2;

    //Nivell 1
    public float forceTorusNivell1;
    public float forced;


    //Nivell 3
    public float forcePendulum;
    public float forceAspa;


    //Nivell 5
    public float forcePorta;
    public float forceRoda;

    //Nivell 4
    public float forceMartell;
    public float forceBoxe; 




    [HideInInspector]
    private bool Falling; 
    float pathState;
    bool colisionat;
    bool fentRestart;
    bool canviantNivell;
    bool guanyatBlue;
    bool perdutBlue; 


    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();
        myRigidbody = GetComponent<Rigidbody>();
        myTransform = GetComponent<Transform>();
        myRigidbody.sleepThreshold = 0.0f;
        canviantNivell = false;
        guanyatBlue = false;
        perdutBlue = false;
        animator.SetBool("isFalling", false);
        animator.SetBool("BlueCry", false);
        animator.SetBool("Climb", false);
        animator.SetBool("BlueWin", false);
        ComensaNivell(1); 

    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "punxes1" || collision.gameObject.name == "punxes2" || collision.gameObject.name == "punxes3" || collision.gameObject.name == "punxes4")
        {
            myRigidbody.AddForce(new Vector3(-1f, 1f, -1f) * forceGrupPunxes1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "punxes8")
        {
            myRigidbody.AddForce(new Vector3(0f, 1f, 1f) * forceGrupPunxes2);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "punxes11")
        {
            myRigidbody.AddForce(new Vector3(-1f, 1f, 0f) * forceGrupPunxes3);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "cGran1")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceGirador1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "cGran2")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceGirador2);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "Torus1" || collision.gameObject.name == "Torus2")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceTorusNivell1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "d2" || collision.gameObject.name == "d1" || collision.gameObject.name == "d3")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forced);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "f11" || collision.gameObject.name == "f22" || collision.gameObject.name == "f33" || collision.gameObject.name == "f44" || collision.gameObject.name == "f55" || collision.gameObject.name == "f66" || collision.gameObject.name == "f77")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forcePendulum);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "pal2aspa1" || collision.gameObject.name == "pal1aspa1" || collision.gameObject.name == "pal1aspa2" || collision.gameObject.name == "pal2aspa2")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceAspa);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "porta11" || collision.gameObject.name == "porta12" || collision.gameObject.name == "porta21" || collision.gameObject.name == "porta22" || collision.gameObject.name == "porta31" || collision.gameObject.name == "porta32" || collision.gameObject.name == "porta41" || collision.gameObject.name == "porta42")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forcePorta);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "Roda1Objecte1" || collision.gameObject.name == "Roda1Objecte2" || collision.gameObject.name == "Roda1Objecte3" || collision.gameObject.name == "Roda1Objecte4" || collision.gameObject.name == "Roda2Objecte1" || collision.gameObject.name == "Roda2Objecte2" || collision.gameObject.name == "Roda2Objecte3" || collision.gameObject.name == "Roda2Objecte4")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceRoda);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "d8")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forced);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "cGran3")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceGirador1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "picMartell1" || collision.gameObject.name == "picMartell2" || collision.gameObject.name == "picMartell3" || collision.gameObject.name == "picMartell4" || collision.gameObject.name == "picMartell5" || collision.gameObject.name == "picMartell6" || collision.gameObject.name == "picMartell7" || collision.gameObject.name == "picMartell8")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceMartell);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "pal2aspa3" || collision.gameObject.name == "pal1aspa3" || collision.gameObject.name == "pal2aspa4" || collision.gameObject.name == "pal1aspa4")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceAspa);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "Torus3")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceTorusNivell1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "picoBoxa1" || collision.gameObject.name == "picoBoxa2" || collision.gameObject.name == "picoBoxa3" || collision.gameObject.name == "picoBoxa4")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceBoxe);
            myRigidbody.useGravity = true;
            colisionat = true;
            animator.SetBool("isMoving", false);
        }

    }


    // Update is called once per frame
    void Update()
    {

        if (!canviantNivell && !guanyatBlue && !perdutBlue)
        {
            if ((Input.GetKey(KeyCode.Alpha1)) && (currentNivell != 1))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                animator.SetBool("isFalling", false);
                StartCoroutine(canviaNivell(1)); 
            }
            else if ((Input.GetKey(KeyCode.Alpha2)) && (currentNivell != 2))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                animator.SetBool("isFalling", false);
                StartCoroutine(canviaNivell(2));
            }
            else if ((Input.GetKey(KeyCode.Alpha3)) && (currentNivell != 3))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                animator.SetBool("isFalling", false);
                StartCoroutine(canviaNivell(3));
            }
            else if ((Input.GetKey(KeyCode.Alpha4)) && (currentNivell != 4))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                animator.SetBool("isFalling", false);
                StartCoroutine(canviaNivell(4));
            }
            else if ((Input.GetKey(KeyCode.Alpha5)) && (currentNivell != 5))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                animator.SetBool("isFalling", false);
                StartCoroutine(canviaNivell(5));
            }
            else
            {
                if (myRigidbody.velocity.y < FallingThreshold)
                {
                    Falling = true;
                    animator.SetBool("isMoving", false);
                }
                else
                {
                    Falling = false;
                }

                if (!Falling && !colisionat && !fentRestart)
                {
                    if (Input.GetKey(KeyCode.UpArrow))
                    {
                        if (currentNivell == 1)
                        {
                            MouNivell1();
                        }
                        else if (currentNivell == 2)
                        {
                            MouNivell2();
                        }
                        else if (currentNivell == 3)
                        {
                            MouNivell3();
                        }
                        else if (currentNivell == 4)
                        {
                            MouNivell4();
                        }
                        else if (currentNivell == 5)
                        {
                            MouNivell5();
                        }
                    }
                    else
                    {
                        animator.SetBool("isMoving", false);
                    }
                }


                else if (colisionat && !fentRestart)
                { //reseteja 
                    animator.SetBool("isFalling", true);
                    fentRestart = true;
                    StartCoroutine(restartNivell());
                }
            }

        }



    }



    private void ComensaNivell(int nivell)
    {
        myRigidbody.useGravity = true;
        myRigidbody.velocity = Vector3.zero;
        myRigidbody.constraints = RigidbodyConstraints.FreezeRotationX | RigidbodyConstraints.FreezeRotationZ;
        myRigidbody.velocity = Vector3.zero;
        Falling = false;
        colisionat = false;
        currentNivell = nivell;
        //posicio i mirar en principi nivell
        pathState = 0f;
        if (nivell == 1)
        {
            Vector3 pathPosition = pathCreator1.path.GetPointAtDistance(pathState);
            //Vector3 pathPosition = pathCreator1.path.GetPointAtDistance(420f);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(5000f, 0f, 0f)); 
        }
        else if (nivell == 2)
        {
            Vector3 pathPosition = pathCreator2.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(0f, 0f, 5000f));
        }
        else if (nivell == 3)
        {
            Vector3 pathPosition = pathCreator3.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(0f, 0f, 5000f));
        }
        else if (nivell == 4)
        {
            Vector3 pathPosition = pathCreator4.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(0f, 0f, -5000f));
        }
        else if (nivell == 5)
        {
            Vector3 pathPosition = pathCreator5.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(5000f , 0f, 0f));
        }
    }

    private void MouNivell1()
    {
        pathState += speed * Time.deltaTime;
        if (pathState > 480f)
        {
            StartCoroutine(guanyat()); 
        }
        else
        {
            Vector3 pathPosition = pathCreator1.path.GetPointAtDistance(pathState);
            Vector3 pathPositionNext = pathCreator1.path.GetPointAtDistance(pathState * 1.01f);
            myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
            transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
        }
    }

    private void MouNivell2()
    {
        pathState += speed * Time.deltaTime;
        if (pathState > 309f)
        {
            StartCoroutine(guanyat());
        }
        else
        {
            Vector3 pathPosition = pathCreator2.path.GetPointAtDistance(pathState);
            Vector3 pathPositionNext = pathCreator2.path.GetPointAtDistance(pathState * 1.01f);
            myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
            transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
        }
    }

    private void MouNivell3()
    {
        pathState += speed * Time.deltaTime;
        if (pathState > 372f)
        {
            StartCoroutine(guanyat());
        }
        else
        {
            Vector3 pathPosition = pathCreator3.path.GetPointAtDistance(pathState);
            Vector3 pathPositionNext = pathCreator3.path.GetPointAtDistance(pathState * 1.01f);
            myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
            transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
        }
    }

    private void MouNivell4()
    {
        pathState += speed * Time.deltaTime;
        Vector3 pathPosition = pathCreator4.path.GetPointAtDistance(pathState);
        Vector3 pathPositionNext = pathCreator4.path.GetPointAtDistance(pathState * 1.01f);
        if (pathState > 387f)
        {
            StartCoroutine(guanyat());
        }
        else if (pathState > 286.0f)
        {
            myRigidbody.useGravity = false; 
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            //transform.LookAt(new Vector3((float)pathPositionNext.x, (float)pathPosition.y, (float)pathPositionNext.z));
            animator.SetBool("Climb", true);
        }
        else
        {
            myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
            transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
            animator.SetBool("Climb", false);
        }
    }

    private void MouNivell5()
    {
        pathState += speed * Time.deltaTime;
        if (pathState > 632f)
        {
            StartCoroutine(guanyat());
        }
        else
        {
            Vector3 pathPosition = pathCreator5.path.GetPointAtDistance(pathState);
            Vector3 pathPositionNext = pathCreator5.path.GetPointAtDistance(pathState * 1.01f);
            myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
            transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
        }

    }

    
    private IEnumerator restartNivell()
    {
        animator.SetBool("Climb", false);
        yield return new WaitForSeconds(2f);
        StartCoroutine(canvasManager.transitionBlueExposureNegre(2f));
        animator.SetBool("isFalling", false);
        yield return new WaitForSeconds(1f);
        myRigidbody.velocity = Vector3.zero;
        ComensaNivell(currentNivell);
        yield return new WaitForSeconds(1f);
        fentRestart = false; 
        yield return null; 
    }

    private IEnumerator canviaNivell(int nivell)
    {
        //yield return new WaitForSeconds(2f);
        animator.SetBool("Climb", false);
        StartCoroutine(volumeManager.transitionExposureBlanc(2f));
        yield return new WaitForSeconds(1f);
        myRigidbody.velocity = Vector3.zero;
        animator.SetBool("BlueWin", false);
        animator.SetBool("BlueCry", false);
        ComensaNivell(nivell);
        yield return new WaitForSeconds(1f);
        canviantNivell = false;
        guanyatBlue = false;
        perdutBlue = false;
        yield return null;
    }

    
    private IEnumerator guanyat()
    {
        StartCoroutine(RedPlayer.perdut()); 
        guanyatBlue = true;
        canviantNivell = true;
        animator.SetBool("BlueWin", true);
        if (currentNivell != 5)
        {
            yield return new WaitForSeconds(3f);
            StartCoroutine(canviaNivell(currentNivell+1));
        }
        else
        {
            //Credits
            yield return null; 
        }


    }


    public IEnumerator perdut()
    {
        perdutBlue = true;
        canviantNivell = true;
        animator.SetBool("BlueCry", true);
        if (currentNivell != 5)
        {
            yield return new WaitForSeconds(3f);
            StartCoroutine(canviaNivell(currentNivell + 1));
        }
        else
        {
            //Credits
            yield return null; 
        }


    }

    public void ComensaPrincipi()
    {
        ComensaNivell(1);
    }


}
